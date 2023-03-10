from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import render

from attendance.forms import AttendanceForm, DivErrorList
from attendance.models import Attendance, Student
from attendance.utils import attendance_cache, refresh_attendance


def render_index(
    request,
    form,
    refresh=False,
    attendance_cache=attendance_cache
):
    if refresh:
        attendance_cache = refresh_attendance()

    return render(
        request,
        'attendance/index.html',
        {'form': form, 'attendance': attendance_cache}
    )


def index(request, refresh=True):
    form = AttendanceForm(error_class=DivErrorList)
    return render_index(request, form, refresh=refresh)


def add_attendance(request):
    if request.method == 'POST':
        data = request.POST
        form = AttendanceForm(data, error_class=DivErrorList)

        if form.is_valid():
            # Get student info
            student_id = data['student_id']
            student = Student.objects.get(student_id=student_id)
            attendance = Attendance(student=student)
            attendance.save()

            welcome = 'Welcome back, %s!' % student.first_name
            messages.success(request, welcome)

            return render_index(request, form, refresh=True)
        else:
            return render_index(request, form, refresh=True)


def get_attendance(request):
    if request.method == 'GET':
        global attendance_cache
        return JsonResponse(list(attendance_cache.values()), safe=False)
