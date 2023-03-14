from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

from attendance.models import student_exists, Attendance


class DivErrorList(ErrorList):

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''

        error_class = 'alert alert-danger'
        return '<div class="errorlist">%s</div>' % ''.join(
            ['<div class="%s">%s</div>' % (error_class, e) for e in self]
        )


class NonstickyTextInput(forms.TextInput):
    """
    Custom text input widget that's "non-sticky"
    (i.e. does not remember submitted values).
    """
    def __init__(self, **kwargs):
        attrs = dict()

        if kwargs['autofocus']:
            attrs.update({
                'placeholder': _('Enter your Student ID'),
                'class': 'form-control',
                'autofocus': True
            })

        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        value = None  # Clear the submitted value.
        return super().get_context(name, value, attrs)


class AttendanceForm(forms.Form):
    student_id = forms.CharField(
        max_length=50,
        label='',
        widget=NonstickyTextInput(autofocus=True)
    )

    def clean_student_id(self):
        # Check if this student exists
        student_id = self.cleaned_data['student_id']
        if not student_exists(student_id):
            raise ValidationError("Student ID not found: %s" % student_id)

        # Check if this student has recently loggedin
        next_min, has_logged = Attendance.has_recent_login(student_id)
        if has_logged:
            unit = 'minute' if next_min == 1 else 'minutes'
            raise ValidationError(
                "Please login again after %s %s." % (next_min, unit)
            )

        return student_id
