from attendance.models import Attendance


def pluralize(count, singular, plural=None):
    if not plural:
        plural = singular + 's'
    unit = singular if float(count) == 1.0 else plural
    return '%s %s' % (count, unit)


def format_timespan(cls, seconds):
    hours, seconds = divmod(seconds, 60*60)
    minutes, seconds = divmod(seconds, 60)

    HH = pluralize(hours, 'hour')
    MM = pluralize(minutes, 'minute')
    SS = pluralize(seconds, 'second')

    if hours:
        return '%s %s' % (HH, MM)
    elif minutes:
        return '%s %s' % (MM, SS)
    else:
        return '%s' % SS


def _get_attendance():
    LIMIT = 5
    attendance = (
        Attendance.objects.all()
        .order_by('-login_ts')
        .select_related('student')
    )
    return attendance[:LIMIT]


def refresh_attendance():
    attendance_cache = _get_attendance()
    return attendance_cache


attendance_cache = refresh_attendance()
