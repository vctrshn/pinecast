from __future__ import absolute_import

import datetime
import json

from django.conf import settings

from .constants import USER_TIMEFRAMES
from .influx import escape, get_client, ident
from pinecast.types import StringTypes


def _get_lone(response, default=-1):
    raw = response.raw
    if not raw:
        return default
    return raw['series'][0]['values'][0][1]

def total_listens(podcast, episode=None):
    podcast_is_str = isinstance(podcast, StringTypes)
    episode_is_str = isinstance(episode, StringTypes)

    if episode:
        condition = 'episode = \'%s\'' % settings.INFLUXDB_CONDITION_OVERRIDES.get(
            'episode', episode if episode_is_str else str(episode.id))
    else:
        condition = 'podcast = \'%s\'' % settings.INFLUXDB_CONDITION_OVERRIDES.get(
            'podcast', podcast if podcast_is_str else str(podcast.id))

    query = 'SELECT COUNT(v) FROM "listen" WHERE %s;' % condition

    base_listens = 0
    if not podcast_is_str:
        if episode and not episode_is_str:
            base_listens = episode.stats_base_listens
        elif not episode:
            base_listens = podcast.stats_base_listens

    val = base_listens
    try:
        val += _get_lone(get_client().query(query, database=settings.INFLUXDB_DB_LISTEN), 0)
    except Exception:
        return -1
    return val


def total_listens_this_week(podcast, tz):
    query = 'SELECT COUNT(v) FROM "listen" WHERE podcast = \'%s\' AND %s;' % (
        settings.INFLUXDB_CONDITION_OVERRIDES.get('podcast', str(podcast.id)),
        USER_TIMEFRAMES['week'](tz))

    try:
        return _get_lone(get_client().query(query, database=settings.INFLUXDB_DB_LISTEN), 0)
    except Exception:
        return -1


def total_subscribers(podcast):
    query = 'SELECT COUNT(v) FROM "subscription" WHERE podcast = \'%s\' AND %s;' % (
        settings.INFLUXDB_CONDITION_OVERRIDES.get('podcast', str(podcast.id)),
        USER_TIMEFRAMES['day'](0)) # tz offset of zero because it doesn't matter which day

    try:
        return _get_lone(get_client().query(query, database=settings.INFLUXDB_DB_SUBSCRIPTION), 0)
    except Exception:
        return -1


def get_top_episodes(podcasts, timeframe=None, tz=None):
    if not isinstance(podcasts, (list, tuple)):
        podcasts = [podcasts]
    if not podcasts:
        return {}

    where_clause = ' OR '.join('podcast = %s' % escape(p) for p in podcasts)
    if timeframe:
        where_clause = '(%s) AND %s' % (where_clause, USER_TIMEFRAMES[timeframe](tz))

    query = 'SELECT COUNT(episode_f) FROM "listen" WHERE %s GROUP BY episode;' % where_clause

    result = get_client().query(query, database=settings.INFLUXDB_DB_LISTEN)

    return {
        tags['episode']: list(v)[0]['count'] for
        (_, tags), v in
        result.items()
    }

def get_episode_sparklines(podcast, tz=None):
    where_clause = "podcast = '%s' AND %s" % (
        settings.INFLUXDB_CONDITION_OVERRIDES.get('podcast', str(podcast.id)),
        USER_TIMEFRAMES['month'](tz))
    query = 'SELECT COUNT(v) FROM "listen" WHERE %s GROUP BY episode, time(1d);' % where_clause

    try:
        result = get_client().query(query, database=settings.INFLUXDB_DB_LISTEN)
    except Exception:
        return {}

    def qualifies(v):
        counts = [float(x['count']) for x in v]
        greatest = max(counts)
        avg = sum(counts) / len(counts)
        return greatest - avg > max(greatest * 0.5, 5)

    return {
        tags['episode']: [x['count'] for x in v] for
        (_, tags), v in
        [(k, list(v)) for k, v in result.items()] if
        qualifies(v)
    }


def rotating_colors(sequence, key='color', highlight_key='highlight'):
    for x, c in zip(sequence, _colors_forever()):
        x[key] = c
        x[highlight_key] = _colorscale(c, 1.1)
        yield x


def _colors_forever():
    while 1:
        yield '#5395D3'
        yield '#52D1C7'
        yield '#FF9800'
        yield '#4CAF50'
        yield '#FF4081'

        yield '#1abc9c'
        yield '#2ecc71'
        yield '#3498db'
        yield '#9b59b6'
        yield '#34495e'
        yield '#16a085'
        yield '#27ae60'
        yield '#2980b9'
        yield '#8e44ad'
        yield '#2c3e50'
        yield '#f1c40f'
        yield '#e67e22'
        yield '#e74c3c'
        yield '#f39c12'
        yield '#d35400'
        yield '#c0392b'


def _colorscale(hexstr, scalefactor):
    """
    Scales a hex string by ``scalefactor``. Returns scaled hex string.

    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.

    >>> colorscale("#DF3C3C", .5)
    #6F1E1E
    >>> colorscale("#52D24F", 1.6)
    #83FF7E
    >>> colorscale("#4F75D2", 1)
    #4F75D2
    """

    hexstr = hexstr.strip('#')

    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    r = max(0, min(r * scalefactor, 255))
    g = max(0, min(g * scalefactor, 255))
    b = max(0, min(b * scalefactor, 255))

    return "#%02x%02x%02x" % (int(r), int(g), int(b))
