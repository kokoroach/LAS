import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    middle_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.get_username()


class Course(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.code


class Student(models.Model):

    class Sex(models.TextChoices):
        MALE = "m", "Male"
        FEMALE = "f", "Female"

    class YearLevel(models.IntegerChoices):
        FIRST = 1, '1'
        SECOND = 2, '2'
        THIRD = 3, '3'
        FOURTH = 4, '4'
        FIFTH = 5, '5'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    student_id = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    year = models.IntegerField(
        choices=YearLevel.choices,
        default=YearLevel.FIRST
    )
    sex = models.CharField(max_length=1, choices=Sex.choices, default=Sex.MALE)

    def __str__(self):
        return str(self.user)

    @classmethod
    def update_or_create_student_user(cls, student_id, data):
        return User.objects.update_or_create(
            username=student_id, defaults=data
        )

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self, student_id=None):
        return self.user.last_name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    login_ts = models.DateTimeField(default=now, verbose_name='Login')

    def __str__(self):
        return str(self.student)

    @classmethod
    def has_recent_login(cls, student_id):
        delta = now() - timedelta(minutes=2)

        attendance = (
            cls.objects
            .filter(student__student_id=student_id,
                    login_ts__gte=delta)
            .order_by('-login_ts')
            .first()
        )
        if attendance:
            actual_delta = attendance.login_ts - delta
            next_min = round((actual_delta.seconds) / 60) or 1
            return (next_min, True)

        return (None, False)


def student_exists(student_id):
    return Student.objects.filter(student_id=student_id).exists()
