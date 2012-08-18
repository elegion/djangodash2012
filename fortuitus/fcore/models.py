from django.db.models.signals import post_save
from autoslug.fields import AutoSlugField
from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    """ Organization. """
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class FortuitusProfile(models.Model):
    """ User profile. """
    user = models.OneToOneField(User)
    # TODO: support multiple organizations.
    company = models.ForeignKey(Company, null=True, blank=True)


def create_user_profile(sender, instance, created, **kwargs):
    """ User post_save signal handler, creates user profile instance. """
    if created:
        FortuitusProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
