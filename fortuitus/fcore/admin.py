from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from fortuitus.fcore.models import Company, FortuitusProfile


class FortuitusProfileInline(admin.StackedInline):
    class Meta:
        model = FortuitusProfile


class UserAdmin(UserAdmin):
    inlines = [FortuitusProfileInline]


admin.site.register(Company)
admin.site.unregister(User)
