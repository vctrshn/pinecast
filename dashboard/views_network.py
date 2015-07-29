from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext, ugettext_lazy
from django.views.decorators.http import require_POST

import podmaster.email
from accounts.models import Network
from podcasts.models import Podcast
from podmaster.helpers import reverse
from views import _pmrender, signer


@login_required
def network_dashboard(req, network_id):
    net = get_object_or_404(Network, deactivated=False, id=network_id, members__in=[req.user])

    ame = ugettext('No user with that email address was found') if req.GET.get('add_member_error') == 'dne' else None
    added_member = req.GET.get('added_member', 'false') == 'true'
    return _pmrender(req,
                     'dashboard/network/netdash.html',
                     {'network': net,
                      'add_member_error': ame,
                      'add_member_success': added_member})


@login_required
def network_add_show(req, network_id):
    net = get_object_or_404(Network, deactivated=False, id=network_id, members__in=[req.user])
    if req.POST:
        slug = req.POST.get('slug')
        try:
            pod = Podcast.objects.get(slug=slug)
        except Podcast.DoesNotExist:
            return _pmrender(req, 'dashboard/network/add_show.html', {'network': net, 'error': ugettext('No podcast with the slug "%s" was found') % slug})
        else:
            if pod.owner != req.user:
                return _pmrender(req, 'dashboard/network/add_show.html', {'network': net, 'error': ugettext('You must be the owner of a podcast to add it to a network')})
            pod.networks.add(net)
            pod.save()
        return redirect('network_dashboard', network_id=net.id)
            
    return _pmrender(req, 'dashboard/network/add_show.html', {'network': net})


@login_required
@require_POST
def network_add_member(req, network_id):
    net = get_object_or_404(Network, deactivated=False, id=network_id, members__in=[req.user])

    try:
        user = User.objects.get(email=req.POST.get('email'))
    except User.DoesNotExist:
        return redirect(reverse('network_dashboard', network_id=network_id) + '?add_member_error=dne#tab-members')

    net.members.add(user)
    net.save()
    podmaster.email.send_notification_email(
        user,
        ugettext('[PodMaster] You have been added to "%s"') % net.name,
        ugettext('''
We are emailing you to let you know that you were added to the network
"%s". No action is required on your part. If you log in to PodMaster,
you will now have read and write access to all of the podcasts in the
network, and will be able to add your own podcasts to the network.
        ''') % net.name
    )

    return redirect(reverse('network_dashboard', network_id=net.id) + '?added_member=true#tab-members')


@login_required
def network_edit(req, network_id):
    net = get_object_or_404(Network, deactivated=False, id=network_id, members__in=[req.user])
    
    if not req.POST:
        return _pmrender(req, 'dashboard/network/edit.html', {'network': net})

    try:
        net.name = req.POST.get('name')
        net.image_url = signer.unsign(req.POST.get('image-url'))
        net.save()
    except Exception:
        return _pmrender(req,
                         'dashboard/network/edit.html',
                         {'network': net, 'error': ugettext('Error while saving network details')})

    return redirect('network_dashboard', network_id=net.id)


@login_required
def network_deactivate(req, network_id):
    net = get_object_or_404(Network, deactivated=False, id=network_id, members__in=[req.user])
    
    if not req.POST:
        return _pmrender(req, 'dashboard/network/deactivate.html', {'network': net})

    if req.POST.get('confirm') != 'doit':
        return redirect('dashboard')

    net.deactivated = True
    net.save()

    return redirect('dashboard')


@login_required
def network_remove_podcast(req, network_id, podcast_slug):
    net = get_object_or_404(Network, deactivated=False, id=network_id, members__in=[req.user])
    pod = get_object_or_404(Podcast, slug=podcast_slug, networks__in=[net])
    
    # We don't need to confirm if the user is the owner.
    if pod.owner == req.user:
        pod.networks.remove(net)
        pod.save()
        return redirect('network_dashboard', network_id=net.id)

    if not req.POST:
        return _pmrender(req, 'dashboard/network/remove_podcast.html', {'network': net, 'podcast': pod})

    if req.POST.get('confirm') != 'doit':
        return redirect('network_dashboard', network_id=net.id)

    pod.networks.remove(net)
    pod.save()

    return redirect('network_dashboard', network_id=net.id)


@login_required
def network_remove_member(req, network_id, member_id):
    net = get_object_or_404(Network, deactivated=False, id=network_id, members__in=[req.user])
    user = get_object_or_404(User, id=member_id)

    if not net.members.filter(username=user.username).count():
        raise Http404()

    pods = Podcast.objects.filter(owner=user, networks__in=[net])
    
    # We don't need to confirm if the user is the owner.
    if net.owner == user:
        return redirect('network_dashboard', network_id=net.id)

    if not req.POST:
        return _pmrender(req, 'dashboard/network/remove_member.html', {'network': net, 'member': user, 'pods': pods})

    if req.POST.get('confirm') != 'doit':
        return redirect('network_dashboard', network_id=net.id)

    for pod in pods:
        pod.networks.remove(net)
        pod.save()
    net.members.remove(user)
    net.save()

    return redirect('network_dashboard', network_id=net.id)
