from __future__ import absolute_import
from __future__ import division

import json
import sys
import time

import iso8601
import rollbar
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import accounts.payment_plans as payment_plans
from .models import RecurringTip, TipEvent
from .stripe_lib import stripe
from accounts.models import UserSettings
from dashboard.views import _pmrender
from notifications.models import NotificationHook
from pinecast.email import CONFIRMATION_PARAM, send_notification_email
from pinecast.helpers import get_object_or_404, json_response, reverse
from podcasts.models import Podcast


BASE_URL = 'https://pinecast.com' if not settings.DEBUG else 'http://localhost:8000'


@login_required
def upgrade(req):
    us = UserSettings.get_from_user(req.user)
    customer = us.get_stripe_customer()

    ctx = {
        'active_coupon': req.session.get('coupon'),
        'coupon_applied': 'coupon_applied' in req.GET,
        'coupon_invalid': 'coupon_invalid' in req.GET,
        'coupon_unavailable': 'coupon_unavailable' in req.GET,
        'error': req.GET.get('error'),
        'stripe_customer': customer,
        'success': 'success' in req.GET,
    }
    return _pmrender(req, 'payments/main.html', ctx)


AVAILABLE_PLANS = {
    'demo': payment_plans.PLAN_DEMO,
    'starter': payment_plans.PLAN_STARTER,
    'pro': payment_plans.PLAN_PRO,
}

@require_POST
@login_required
def upgrade_set_plan(req):
    new_plan = req.POST.get('plan')
    if new_plan not in AVAILABLE_PLANS:
        return redirect('upgrade')

    new_plan_val = AVAILABLE_PLANS[new_plan]

    us = UserSettings.get_from_user(req.user)
    result = us.set_plan(new_plan_val, req.session.get('coupon'))

    if not result:
        return redirect('upgrade')
    elif result == 'card_error':
        return redirect(reverse('upgrade') + '?error=card')
    else:
        req.session['coupon'] = None
        return redirect(reverse('upgrade') + '?success')


@require_POST
@login_required
def set_coupon(req):
    code = req.POST.get('coupon')
    try:
        coupon = stripe.Coupon.retrieve(code)
    except stripe.error.InvalidRequestError:
        return redirect(reverse('upgrade') + '?coupon_invalid')

    if not coupon.valid:
        return redirect(reverse('upgrade') + '?coupon_invalid')

    if 'owner_id' in coupon.metadata:
        us = UserSettings.get_from_user(req.user)
        if us.plan != payment_plans.PLAN_DEMO:
            return redirect(reverse('upgrade') + '?coupon_unavailable')

        try:
            cust = us.get_stripe_customer()
        except Exception:
            pass
        else:
            if len(stripe.Invoice.list(customer=cust.id, limit=1).data):
                return redirect(reverse('upgrade') + '?coupon_unavailable')

    req.session['coupon'] = code
    return redirect(reverse('upgrade') + '?coupon_applied')


@require_POST
@login_required
def set_payment_method_redir(req):
    us = UserSettings.get_from_user(req.user)
    customer = us.get_stripe_customer()

    if req.POST.get('next_url') == 'upgrade':
        next_url = reverse('upgrade')
    else:
        next_url = reverse('dashboard') + '?success=csuc#settings'

    try:
        if customer:
            customer.source = req.POST.get('token')
            customer.save()
        else:
            us.create_stripe_customer(req.POST.get('token'))
    except stripe.error.CardError as e:
        return redirect(next_url + '?error=crej#settings')
    except Exception as e:
        rollbar.report_exc_info(sys.exc_info(), req)
        return redirect(next_url + '?error=cerr#settings')

    return redirect(next_url)


@require_POST
@login_required
@json_response
def set_tip_cashout(req):
    try:
        dob = iso8601.parse_date(req.POST.get('dob'))
    except Exception:
        return {'success': False, 'error': 'invalid dob'}

    forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        ip = forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')

    legal_entity = {
        'address': {
            'city': req.POST.get('addressCity'),
            'state': req.POST.get('addressState'),
            'postal_code': req.POST.get('addressZip'),
            'line1': req.POST.get('addressStreet'),
            'line2': req.POST.get('addressSecond'),
        },
        'ssn_last_4': req.POST.get('ssnLastFour'),
        'dob': {
            'day': dob.day,
            'month': dob.month,
            'year': dob.year,
        },
        'first_name': req.POST.get('firstName'),
        'last_name': req.POST.get('lastName'),
        'type': 'individual',
    }

    us = UserSettings.get_from_user(req.user)
    account = us.get_stripe_managed_account()
    if account:
        account.external_account = req.POST.get('token')
        for key in legal_entity:
            setattr(account.legal_entity, key, legal_entity[key])
        account.save()
    else:
        us.create_stripe_managed_account(
            req.POST.get('token'), ip, legal_entity)

    return {'success': True}


@csrf_exempt
@require_POST
@json_response
def hook(req):
    try:
        body = json.loads(req.body.decode('utf-8'))
    except Exception as e:
        rollbar.report_message(
            'Error parsing Stripe hook JSON: %s' % str(e), 'warn')
        return HttpResponse(status=400)

    if not settings.DEBUG:
        try:
            # Validate the event
            stripe.Event.retrieve(
                body['id'], stripe_account=body.get('user_id'))
        except Exception as e:
            rollbar.report_message(
                'Error fetching Stripe event: %s' % str(e), 'warn')
            return HttpResponse(status=400)


    if body['type'] == 'invoice.payment_succeeded' and body.get('user_id'):
        sub = _get_tip_subscription(body)
        if not sub: return {'warning': 'subscription unrecognized'}

        amount = int(body['data']['object']['total'])
        pod = sub.podcast

        tip_event = TipEvent(
            tipper=sub.tipper,
            podcast=pod,
            amount=amount,
            recurring_tip=sub)
        tip_event.save()

        Podcast.objects.filter(id=pod.id).update(total_tips=F('total_tips') + amount)

        email = sub.tipper.email_address
        send_notification_email(
            None,
            ugettext('Thanks for leaving a tip!'),
            ugettext('Your tip was sent: %s received $%0.2f. Thanks for supporting your '
                     'favorite content creators!') % (pod.name, float(amount) / 100),
            email=email)
        send_notification_email(
            pod.owner,
            ugettext('%s received a tip of $%0.2f') % (pod.name, float(amount) / 100),
            ugettext('%s received a tip of $%0.2f from %s as part of a monthly '
                     'subscription to the show. You should send them an email '
                     'thanking them for their generosity.') %
                (pod.name, float(amount) / 100, email))

        NotificationHook.trigger_notification(
            podcast=pod,
            trigger_type='tip',
            data={'tipper': sub.tipper.email_address,
                  'amount': amount})

        return {'success': 'emails sent, tip event processed'}

    elif body['type'] == 'invoice.payment_succeeded':
        sub = stripe.Subscription.retrieve(body['data']['object']['subscription'])
        if not sub.discount:
            return {'success': 'ignoring undiscounted subscription'}

        coupon_code = sub.discount.coupon.id
        try:
            coupon_owner = UserSettings.objects.get(coupon_code=coupon_code)
        except UserSettings.DoesNotExist:
            return {'success': 'coupon not owned by referrer'}

        if coupon_owner.plan == payment_plans.PLAN_DEMO or coupon_owner.plan == payment_plans.PLAN_COMMUNITY:
            return {'success': 'coupon owned by free user'}

        min_charge = float('inf')
        valid_charges = 0

        # We limit this to three. If it goes over or under, we can ignore the charge.
        invoices = stripe.Invoice.list(customer=sub.customer, limit=3)
        if len(invoices.data) < 2:
            return {'success': 'did not reach two invoices yet'}

        for invoice in invoices.data:
            if not invoice.paid:
                continue
            valid_charges += 1

            invoice_amount = 0
            for line in invoice.lines.data:
                invoice_amount += line.amount
            if invoice_amount < min_charge:
                min_charge = invoice_amount

        if valid_charges != 2:
            return {'success': 'did not have two successful invoices'}

        try:
            owner_cust = coupon_owner.get_stripe_customer()
        except Exception as e:
            rollbar.report_message('Error fetching coupon owner stripe customer: %s' % str(e), 'error')
            return {'success': 'coupon owner does not exist'}
        else:
            if not owner_cust:
                rollbar.report_message('Coupon owner did not have valid stripe customer', 'error')
                return {'success': 'coupon owner does not exist'}

        amount = min_charge * 2

        # Negative amounts are credits
        owner_cust.account_balance -= amount
        owner_cust.save()

        send_notification_email(
            coupon_owner.user,
            ugettext('You have referral credit!'),
            ugettext('One of your referrals has crossed their two-month mark '
                     'as a paying customer. Your account has been credited '
                     '$%.2f.') % (float(amount) / 100))

        return {'success': 'user credited'}

    elif body['type'] == 'invoice.payment_failed':
        if body.get('user_id'):
            return _handle_failed_tip_sub(body)
        else:
            return _handle_failed_subscription(body)

    return {'success': 'ignored'}


def _get_tip_subscription(event_body):
    sub_id = event_body['data']['object']['subscription']
    try:
        return RecurringTip.objects.get(stripe_subscription_id=sub_id)
    except RecurringTip.DoesNotExist:
        rollbar.report_message(
            'Event on unknown subscription: %s' % sub_id, 'warn')
        return None


def _handle_failed_tip_sub(body):
    sub = _get_tip_subscription(body)
    if not sub: return {'warning': 'subscription unrecognized'}

    closed = body['data']['object']['closed']
    pod = sub.podcast
    if closed:
        sub.deactivated = True
        sub.save()

        send_notification_email(
            None,
            ugettext('Your subscription to %s was cancelled') % pod.name,
            ugettext('We attempted to charge your card for your '
                     'subscription to %s, but the payment failed multiple '
                     'times. If you wish to remain subscribed, please '
                     'visit the link below to enter new payment '
                     'information.\n\n%s') %
                (pod.name, BASE_URL + reverse('tip_jar', podcast_slug=pod.slug)),
            email=sub.tipper.email_address)

        return {'success': 'nastygram sent, subscription deactivated'}
    else:
        send_notification_email(
            None,
            ugettext('Your subscription to %s has problems') % pod.name,
            ugettext('We attempted to charge your card for your '
                     'subscription to %s, but the payment failed. Please '
                     'visit the tip jar and update your subscription with '
                     'new card details as soon as possible. You can do that '
                     'at the link below.\n\n%s') %
                (pod.name, BASE_URL + reverse('tip_jar', podcast_slug=pod.slug)),
            email=sub.tipper.email_address)

        return {'success': 'nastygram sent'}


def _handle_failed_subscription(body):
    customer = body['data']['object']['customer']
    try:
        us = UserSettings.objects.get(stripe_customer_id=customer)
    except UserSettings.DoesNotExist:
        rollbar.report_message('Unknown customer: %s' % customer, 'warn')
        return {'warning': 'customer unrecognized'}

    closed = body['data']['object']['closed']
    user = us.user
    if closed:
        us.set_plan(payment_plans.PLAN_DEMO)
        send_notification_email(
            user,
            ugettext('Your Pinecast subscription was cancelled.'),
            ugettext('Pinecast attempted to charge your payment card multiple '
                     'times, but was unable to collect payment. Your '
                     'account has been downgraded to a free Demo plan. Only '
                     'the ten most recent episodes from each of your podcasts '
                     'will be shown to your listeners. All recurring tip '
                     'subscriptions to your podcasts have also been '
                     'cancelled.\n\nNo content or settings have been deleted '
                     'from your account. If you wish to re-subscribe, you may '
                     'do so at any time at the URL below.\n\n%s') %
                (BASE_URL + reverse('upgrade')))

        return {'success': 'nastygram sent, account downgraded'}
    else:
        send_notification_email(
            user,
            ugettext('Payment failed for Pinecast subscription'),
            ugettext('Pinecast attempted to charge your payment card for your '
                     'current subscription, but was unable to collect payment. '
                     'If we fail to process your card three times, your '
                     'account will automatically be downgraded to a free Demo '
                     'plan.\n\n'
                     'No changes have currently been made to your account or '
                     'plan. Please update your payment information at the URL '
                     'below.\n\n%s') %
                (BASE_URL + reverse('dashboard') + '#settings,subscription'))
        return {'success': 'nastygram sent'}
