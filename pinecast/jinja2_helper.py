from __future__ import absolute_import
from __future__ import division

import datetime
import hashlib
import json

import gfm
import jinja2
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.translation import ugettext, ugettext_lazy, ungettext
from jinja2 import Environment, evalcontextfilter

import accounts.payment_plans as payment_plans
from . import helpers
from accounts.models import UserSettings


def environment(**options):
    options['autoescape'] = True

    # Enable localization
    options.setdefault('extensions', [])
    if 'jinja2.ext.i18n' not in options['extensions']:
        options['extensions'].append('jinja2.ext.i18n')

    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,

        'dir': dir,
        'float': float,
        'int': int,
        'len': len,
        'list': list,
        'min': min,
        'max': max,
        'now': lambda hours=0: datetime.datetime.now() + datetime.timedelta(hours=hours),
        'sorted': sorted,
        'str': str,
        'url': helpers.reverse,
        'gravatar': gravatar,
        'getattr': getattr,

        '_': ugettext,
        'gettext': ugettext,
        'ngettext': ungettext,
        'get_user_settings': UserSettings.get_from_user,
        'minimum_plan': minimum_plan,
        'PLAN_NAMES': payment_plans.PLANS_MAP,
        'PLANS': payment_plans.PLANS_RAW,
        'PLAN_MAX_FILE_SIZE': payment_plans.MAX_FILE_SIZE,

        'SUPPORT_URL': settings.SUPPORT_URL,
        'RECAPTCHA_KEY': settings.RECAPTCHA_KEY,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,

        'timezones': [
            -12.0,
            -11.0,
            -10.0,
            # -9.5,
            -9.0,
            -8.0,
            -7.0,
            -6.0,
            -6.0,
            -5.0,
            -4.0,
            # -3.5,
            -3.0,
            -2.0,
            -1.0,
            0,
            1.0,
            2.0,
            3.0,
            # 3.5,
            4.0,
            # 4.5,
            5.0,
            # 5.5,
            6.0,
            # 6.5,
            7.0,
            8.0,
            # 8.5,
            # 8.75,
            9.0,
            # 9.5,
            10.0,
            # 10.5,
            11.0,
            12.0,
            # 12.75,
            13.0,
            14.0,
        ],
    })
    env.filters['format_tz'] = format_tz
    env.filters['https'] = lambda s: ('https:%s' % s[5:]) if s.startswith('http:') else s
    env.filters['json'] = json.dumps
    env.filters['safe_json'] = safe_json
    env.filters['markdown'] = gfm.markdown
    env.filters['pretty_date'] = helpers.pretty_date
    env.filters['sanitize'] = helpers.sanitize
    env.filters['replace'] = lambda s: s.replace
    env.filters['sparkline'] = sparkline
    return env


TZ_SHORTHAND = {
    -8.0: ugettext_lazy('PST'),
    -7.0: ugettext_lazy('MST'),
    -6.0: ugettext_lazy('CST'),
    -5.0: ugettext_lazy('EST'),
}

def format_tz(tz):
    if tz == 0:
        return 'UTC'
    offset = '%d:%0.2d' % (abs(int(tz)), tz % 1 * 60)
    sign = '+' if tz > 0 else '-'
    return 'UTC%s%s%s' % (sign, offset, ' (%s)' % TZ_SHORTHAND[tz] if tz in TZ_SHORTHAND else '')

def minimum_plan(user_settings, plan):
    if isinstance(user_settings, User):
        user_settings = UserSettings.get_from_user(user_settings)
    return payment_plans.minimum(user_settings.plan, plan)


def gravatar(s, size=40):
    dig = hashlib.md5(s.encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/%s?s=%d' % (dig, size)


def safe_json(data):
    if data is None:
        return 'null'
    elif isinstance(data, bool):
        return 'true' if data else 'false'
    elif isinstance(data, (int, float)):
        return str(data)
    elif isinstance(data, (tuple, list)):
        return jinja2.Markup('[%s]' % ','.join(safe_json(x) for x in data))
    elif isinstance(data, dict):
        return jinja2.Markup('{%s}' % ','.join(
            '%s:%s' % (safe_json(key), safe_json(val)) for key, val in data.items()))
    safe_data = str(jinja2.escape(data))
    return jinja2.Markup(json.dumps(safe_data))

def sparkline(data, spacing=1, height=20):
    data = list(data) or [0 for _ in range(31)]
    spark_min = min(data)
    spark_max = max(data)
    spark_range = spark_max - spark_min or 1
    sadj = ((i - spark_min) / spark_range for i in data)
    return ' '.join('%d,%d' % (i * spacing, (1 - y) * height) for i, y in enumerate(sadj))
