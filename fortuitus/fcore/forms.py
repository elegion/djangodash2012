from django import forms
from django.contrib.auth.forms import UserCreationForm

from fortuitus.fcore.models import Company


class RegistrationForm(UserCreationForm):
    """ ModelForm for registration. """
    company = forms.CharField('company', required=True)

    def clean_company(self):
        name = self.cleaned_data['company']
        companies = Company.objects.filter(name=name).count()
        if companies:
            raise forms.ValidationError(
                'This company name is already registered.')
        return name

    def save(self, *args, **kwargs):
        user = super(RegistrationForm, self).save(*args, **kwargs)
        company = Company.objects.create(name=self.cleaned_data['company'])
        user.fortuitusprofile.company = company
        user.fortuitusprofile.save()
        return user
