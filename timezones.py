#!/usr/bin/python
#
# Example of how to use pytz.

import pytz
import time
import calendar
from datetime import datetime, timedelta

FIN = pytz.timezone('Europe/Helsinki')
SWE = pytz.timezone('Europe/Stockholm')
UTC = pytz.utc


def change_timezone(dtobject, tmzone):
    """
    Convert UTC datetime object to a certain timezone.
    """
    if dtobject.tzinfo is not None:
        return tmzone.normalize(dtobject.astimezone(tmzone))

    # Presume that dtobject is UTC, if tzinfo is not declared.
    return pytz.utc.localize(dtobject).astimezone(tmzone)


def datetime_to_utc_unixtime(dtobject):
    """
    Converts timezone-aware dtobject to unix timestamp.
    Adds tzinfo to unixtime.
    """
    naive = dtobject.replace(tzinfo=None)
    return calendar.timegm(datetime.utctimetuple(naive))


def datetime_to_unixtime(dtobject):
    """
    Convert datetime object to unix timestamp. Drops tzinfo.
    """
    return calendar.timegm(datetime.utctimetuple(dtobject))


def unixtime_to_datetime(unixtime):
    """
    Convert unix timestamp to datetime object.
    """
    return datetime.fromtimestamp(unixtime, tz=pytz.utc)


if __name__ == '__main__':
    # UTC unix timestamp, very precise
    utc_unixtime = time.time()

    # UTC unix timestamp, basically floor of time.time()
    utc_unixtime = datetime_to_unixtime(datetime.utcnow())

    # Timezone-aware datetime objects, christmas eve 2011, 18:00:00 UTC
    utc_christmas = change_timezone(datetime(2011, 12, 24, 18, 00, 00), UTC)
    fin_christmas = change_timezone(utc_christmas, FIN)  # Helsinki
    swe_christmas = change_timezone(fin_christmas, SWE)  # Stockholm

    print('Christmas 24/12/2011 18:00:00(UTC) ' +
          'in timezone-aware datetime objects:')
    print('UTC:       %s' % utc_christmas)
    print('Stockholm: %s' % swe_christmas)
    print('Helsinki:  %s' % fin_christmas)
    print('')

    # This demonstrates how datetime_to_unixtime() function returns
    # the same unixtime for datetime objects with different tzinfos.
    print('Real time difference between ' +
          'Helsinki and Stockholm is %s seconds.' %
          abs(datetime_to_unixtime(fin_christmas) -
              datetime_to_unixtime(swe_christmas)))

    # This demonstrates how datetime_to_utc_unixtime()
    # function "adds" the datetime object\'s tzinfo to the unixtime.
    print('Timezone difference between Helsinki and Stockholm is %s seconds.' %
          abs(datetime_to_utc_unixtime(fin_christmas) -
              datetime_to_utc_unixtime(swe_christmas)))
    print('')

    # Demostrate how to add time to a datetime object.
    delay = timedelta(seconds=3600)
    dtobject = datetime.utcnow() + delay
    print('Now + 1 hour in Helsinki:  %s' % change_timezone(dtobject, FIN))
    print('Now + 1 hour in Stockholm: %s' % change_timezone(dtobject, SWE))
    print('')

    days = 200
    print('Lets add %s days to all christmas datetime objects and show them' %
          days)
    print('in UTC format. All of the following results should be the same.')
    delay = timedelta(days=days)  # This skips to year 2012
    delayed_fin_christmas = fin_christmas + delay
    delayed_swe_christmas = swe_christmas + delay
    delayed_utc_christmas = utc_christmas + delay
    print('%s + %s days in UTC: %s' % (fin_christmas, days,
          change_timezone(delayed_fin_christmas, UTC)))
    print('%s + %s days in UTC: %s' % (swe_christmas, days,
          change_timezone(delayed_swe_christmas, UTC)))
    print('%s + %s days in UTC: %s' % (utc_christmas, days,
          change_timezone(delayed_utc_christmas, UTC)))
    print('')

    print('Components separated:')
    print('%s/%s/%s %s:%s:%s (%s)' % (delayed_utc_christmas.day,
          delayed_utc_christmas.month, delayed_utc_christmas.year,
          delayed_utc_christmas.hour, delayed_utc_christmas.minute,
          delayed_utc_christmas.second,
          delayed_utc_christmas.tzinfo))

    print('With strftime:')
    print(delayed_utc_christmas.strftime('%d/%m/%Y %H:%M:%S (%Z)'))
    print(delayed_fin_christmas.strftime('%d/%m/%Y %H:%M:%S (' +
          str(delayed_fin_christmas.tzinfo) + ')'))
