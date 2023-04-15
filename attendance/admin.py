# Django
from django import forms
from django.db.models import Count
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
# from django.utils.translation import gettext_lazy as _

# Third-party
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget

# In-app
from .models import Attendance, AttendanceSummary, Course, Student, User


class StudentForm(forms.ModelForm):

    def save(self, commit=True):
        student_id = self.cleaned_data.get('student_id')

        # Performs create
        if student_id:
            Student.update_or_create_student_user(student_id, {})
            user = User.objects.get(username=student_id)
            self.instance.user = user
        # Performs update
        else:
            # Process as-is
            pass

        return super(StudentForm, self).save(commit=commit)

    class Meta:
        model = Student
        exclude = ('user',)


class CustomUserAdmin(UserAdmin):
    model = User

    readonly_fields = ('id',)
    list_display = (
        'username', 'first_name', 'last_name', 'is_superuser', 'is_staff'
    )

    @property
    def fieldsets(self):
        '''Update fieldset'''
        new_fieldsets = list()
        for fieldset, properties in UserAdmin.fieldsets:
            match fieldset:
                case None:
                    properties['fields'] = ('id', 'username', 'password')
                case 'Personal info':
                    # Include middle_name
                    properties['fields'] = (
                        'first_name', 'middle_name', 'last_name', 'email'
                    )
            new_fieldsets.append((fieldset, properties))
        return tuple(new_fieldsets)


class CourseAdmin(ExportMixin, ModelAdmin):
    list_display = ('code', 'name')


class StudentAdmin(ExportMixin, ModelAdmin):
    form = StudentForm

    _readonly_fields = ('user', 'student_id', '_last_name', '_first_name')
    list_display = (
        'user', '_last_name', '_first_name', 'course', 'year', 'student_id'
    )
    search_fields = ['student_id', 'user__first_name', 'user__last_name']
    list_filter = ['course', 'year']

    @admin.display(ordering='user__first_name', description='First Name')
    def _first_name(self, obj):
        return obj.user.first_name

    @admin.display(ordering='user__last_name', description='Last Name')
    def _last_name(self, obj):
        return obj.user.last_name

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self._readonly_fields
        return ()


class AttendanceResource(ModelResource):

    _id = Field(column_name="ID", attribute="id")
    student = Field(
        column_name="Student ID",
        attribute="student",
        widget=ForeignKeyWidget(Student, field='student_id')
    )
    last_name = Field(
        column_name="Last Name",
        attribute="student__user",
        widget=ForeignKeyWidget(User, field='last_name')
    )
    first_name = Field(
        column_name="Last Name",
        attribute="student__user",
        widget=ForeignKeyWidget(User, field='first_name')
    )
    course = Field(
        column_name="Course",
        attribute="student",
        widget=ForeignKeyWidget(Student, field='course')
    )
    year = Field(
        column_name="Year",
        attribute="student",
        widget=ForeignKeyWidget(Student, field='year')
    )
    login = Field(column_name="Login", attribute="login_ts")

    class Meta:
        model = Attendance
        fields = (
            '_id', 'student', 'last_name', 'first_name', 'course',
            'year', 'login'
        )


class AttendanceAdmin(ExportMixin, ModelAdmin):
    list_display = (
        'student', '_last_name', '_first_name', 'get_course', 'get_year',
        'login_ts'
    )
    list_filter = ('student__course', 'student__year')
    search_fields = [
        'student__student_id', 'student__user__first_name',
        'student__user__last_name'
    ]

    _readonly_fields = ('student',)
    raw_id_fields = ('student',)
    resource_class = AttendanceResource

    @admin.display(ordering='student__course', description='Course')
    def get_course(self, obj):
        return obj.student.course

    @admin.display(ordering='student__year', description='Year')
    def get_year(self, obj):
        return obj.student.year

    @admin.display(
        ordering='student__user__first_name',
        description='First Name'
    )
    def _first_name(self, obj):
        return obj.student.first_name

    @admin.display(
        ordering='student__user__last_name',
        description='Last Name'
    )
    def _last_name(self, obj):
        return obj.student.last_name

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self._readonly_fields
        return ()


class AttendanceSummaryAdmin(ModelAdmin):
    """
    # Custom Attendance Summary Dashboard
    # from: https://hakibenita.medium.com/how-to-turn-django-admin-into-a-lightweight-dashboard-a0e0bbf609ad
    """

    change_list_template = 'admin/attendance_summary_change_list.html'
    date_hierarchy = 'login_ts'

    # Disable Add Model button
    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        # ------------------
        # Student Summary
        # ------------------
        student_qs = (
            qs
            .values('student__id')
            .aggregate(unique_attendees=Count('student__id', distinct=True))
        )
        student_qs['total_students'] = Student.objects.all().count()

        response.context_data['student_summary'] = dict(student_qs)

        # ------------------
        # Course Summary
        # ------------------
        metrics = {
            'total_attendance': Count('student__course__name')
        }
        response.context_data['summary'] = list(
            qs
            .values('student__course__code', 'student__course__name')
            .annotate(**metrics)
            .order_by('-total_attendance')
        )
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(AttendanceSummary, AttendanceSummaryAdmin)
