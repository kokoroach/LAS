# Generated by Django 4.1.5 on 2023-04-15 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_student_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Attendance Summary',
                'verbose_name_plural': 'Attendance Summary',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('attendance.attendance',),
        ),
    ]
