from django import forms

from fortuitus.feditor.models import TestCase


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        exclude = ('project',)
