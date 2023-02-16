import os
import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from attendance.models import Student, Course, student_exists
from attendance.utils import split_name


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        data_file = options['file']

        if not os.path.isfile(data_file):
            raise FileNotFoundError('Please check file path')

        with open(data_file, encoding='utf-8-sig') as csv_file:
            # reading the csv file using DictReader
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self.add_student(row)

    def add_student(self, student):
        # Get student info
        last_name, other_name = student['Student Name'].split(',')
        last_name = last_name.strip().title()
        first_name, middle_name = split_name(other_name)
        student_id = student['ID No.']
        course_code = student['Course']
        year = int(student['Year'][0])

        _user = {
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
        }
        course, _ = Course.objects.get_or_create(code=course_code)

        if not student_exists(student_id):
            with transaction.atomic():
                user = Student.create_student_user(student_id, **_user)
                student = Student.objects.create(
                    user=user,
                    student_id=student_id,
                    course=course,
                    year=year
                )
