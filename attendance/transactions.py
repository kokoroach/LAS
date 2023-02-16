
from .models import Attendance, Student


class AttendanceManager:

    def __init__(self) -> None:
        pass

    def create_attendance(self, barcode):
        student = Student.objects.get(barcode=barcode)
        Attendance.objects.create(student=student)


manager = AttendanceManager()
