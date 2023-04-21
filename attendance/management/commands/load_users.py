import os
import csv
import re

from django.core.management.base import BaseCommand
from django.db import transaction

from attendance.models import User, Student, Course, student_exists


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
        sex = 'm' if student['Sex'].lower() == 'male' else 'f'
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
                Student.update_or_create_student_user(student_id, _user)
                user = User.objects.get(username=student_id)

                student = Student.objects.create(
                    user=user,
                    student_id=student_id,
                    sex=sex,
                    course=course,
                    year=year
                )
