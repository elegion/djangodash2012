from django.contrib import admin
from fortuitus.feditor.models import TestProject, TestCase
from fortuitus.feditor.models import TestCaseAssert, TestCaseStep


class TestCaseStepInline(admin.StackedInline):
    model = TestCaseStep


class TestCaseStepAssert(admin.StackedInline):
    model = TestCaseAssert


class TestCaseAdmin(admin.ModelAdmin):
    inlines = [TestCaseStepInline, TestCaseStepAssert]


admin.site.register(TestProject)
admin.site.register(TestCase, TestCaseAdmin)