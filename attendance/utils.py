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
