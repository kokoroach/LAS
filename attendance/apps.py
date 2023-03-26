from django.apps import AppConfig
from django.db.models.signals import post_migrate

from LAS.management import assign_group_permissions


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'

    group_permissions = [
        (
            'staff_admin', {
                'attendance': ['add', 'change', 'delete', 'view'],
                'student': ['view'],
                'course': ['view'],
            }
        ),
    ]
    for group_name, permissions in group_permissions:
        post_migrate.connect(
            assign_group_permissions(name, group_name, permissions)
        )
