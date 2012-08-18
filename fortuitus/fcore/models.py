from django.db.models.signals import post_save
from autoslug.fields import AutoSlugField
from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class FortuitusProfile(models.Model):
    user = models.OneToOneField(User)

    company = models.ForeignKey(Company, null=True, blank=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FortuitusProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)