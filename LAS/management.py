from django import apps as global_apps
from django.db.models import Q


def assign_group_permissions(app_label, group_name, permissions):

    def receiver(*args, apps=global_apps, **kwargs):
        try:
            Group = apps.get_model('auth', 'Group')
            Permission = apps.get_model('auth', 'Permission')
        except LookupError:
            return

        perm_q = Q()
        for model, perm_types in permissions.items():
            for perm_type in perm_types:
                codename = '%s_%s' % (perm_type, model)
                perm_q |= (
                    Q(content_type__app_label=app_label)
                    & Q(codename=codename)
                )

        group, _ = Group.objects.get_or_create(name=group_name)
        group.permissions.add(
            *Permission.objects.filter(perm_q)
        )

    return receiver
