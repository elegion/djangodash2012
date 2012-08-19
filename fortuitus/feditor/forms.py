from django import forms

from fortuitus.feditor.models import TestCase


class TestCaseForm(forms.ModelForm):
    """ ModelForm for TestCase model. """
    class Meta:
        model = TestCase
        exclude = ('project',)
