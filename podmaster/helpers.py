from functools import wraps

import django.core.urlresolvers
import pytz
from django.core.urlresolvers import reverse as reverse_django
from django.http import JsonResponse


def json_response(*args, **jr_kwargs):
    def wrapper(view):
        @wraps(view)
        def func(*args, **kwargs):
            resp = view(*args, **kwargs)
            if not isinstance(resp, (dict, list, bool, str, unicode, int, float)):
                # Handle HttpResponse/HttpResponseBadRequest/etc
                return resp
            return JsonResponse(resp, safe=jr_kwargs.get('safe', True))
        return func
    return wrapper if jr_kwargs else wrapper(*args)


@wraps(reverse_django)
def reverse(viewname, kwargs=None, **kw):
    if kwargs is None:
        kwargs = {}
    kwargs.update(kw)
    return reverse_django(viewname, kwargs=kwargs)


def tz_offset(tz_name):
    offset = pytz.timezone(tz_name)._utcoffset
    return offset.seconds // 3600 + offset.days * 24