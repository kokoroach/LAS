import re

from attendance.models import Attendance


def _get_attendance():
    limit = 5
    attendance = (
        Attendance.objects.all()
        .order_by('-login_ts')
        .select_related('student')
    )
    return attendance[:limit]


def refresh_attendance():
    attendance_cache = _get_attendance()
    return attendance_cache


attendance_cache = refresh_attendance()


LNAME_PREFIX = ['DE LO', 'DE LA', 'DE LAS', 'DEL', 'DOS', 'DAS', 'DE', 'DELAS']


def split_name(name):
    name = name.upper()
    form = "(.*)({}(.+))".format("(" + " |".join(LNAME_PREFIX) + ")")

    def sanitized_name(names):
        return [name.strip().title() for name in names]

    f1 = re.compile(form)
    m1 = f1.match(name)
    if m1:
        if len(m1.group(1)) != 0:
            name = [m1.group(1), m1.group(2)]
        else:
            name = [name.split()[-1], " ".join(name.split()[:-1])]
    else:
        if len(name.split()) == 1:
            # No middle name
            name = [name, '']
        else:
            name = [" ".join(name.split()[:-1]), name.split()[-1]]

    return sanitized_name(name)
