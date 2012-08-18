from django import forms

from fortuitus.fcore.forms import BootstrapFormMixin
from fortuitus.feditor.models import TestCase


class TestCaseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TestCase
        exclude = ('project',)