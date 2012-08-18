from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from fortuitus.fcore.models import Company, FortuitusProfile


class FortuitusProfileInline(admin.StackedInline):
    """ Users profile admin inline. """
    model = FortuitusProfile


class UserAdmin(UserAdmin):
    """ Users administration. """
    inlines = [FortuitusProfileInline]


admin.site.register(Company)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
