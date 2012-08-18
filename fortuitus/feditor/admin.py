from django.contrib import admin
from fortuitus.feditor.models import TestProject, TestCase
from fortuitus.feditor.models import TestCaseAssert, TestCaseStep


class TestCaseStepInline(admin.StackedInline):
    """ Test case steps administration. """
    model = TestCaseStep


class TestCaseStepAssert(admin.StackedInline):
    """ Test case assertions administration. """
    model = TestCaseAssert


class TestCaseAdmin(admin.ModelAdmin):
    """ Test case administration. """
    inlines = [TestCaseStepInline, TestCaseStepAssert]


admin.site.register(TestProject)
admin.site.register(TestCase, TestCaseAdmin)
