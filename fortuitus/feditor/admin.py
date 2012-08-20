from django.contrib import admin

from fortuitus.feditor.models import TestProject, TestCase
from fortuitus.feditor.models import TestCaseAssert, TestCaseStep


class TestCaseInline(admin.StackedInline):
    model = TestCase


class TestProjectAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]


class TestCaseStepInline(admin.StackedInline):
    model = TestCaseStep


class TestCaseAdmin(admin.ModelAdmin):
    inlines = [TestCaseStepInline]


class TestCaseAssertInline(admin.StackedInline):
    """ Test case assertions administration. """
    model = TestCaseAssert


class TestCaseStepAdmin(admin.ModelAdmin):
    """ Test case steps administration. """
    inlines = [TestCaseAssertInline]

    list_display = ('testcase', 'order', '__unicode__')
    list_display_links = ('__unicode__',)
    list_filter = ('testcase__project', 'testcase',)


admin.site.register(TestProject, TestProjectAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestCaseStep, TestCaseStepAdmin)
