from django.contrib import admin

from fortuitus.feditor.models import TestProject, TestCase
from fortuitus.feditor.models import TestCaseAssert, TestCaseStep


class TestCaseAssertInline(admin.StackedInline):
    """ Test case assertions administration. """
    model = TestCaseAssert


class TestCaseStepAdmin(admin.ModelAdmin):
    """ Test case steps administration. """
    inlines = [TestCaseAssertInline]

    list_display = ('testcase', '__unicode__')
    list_display_links = ('__unicode__',)
    list_filter = ('testcase',)


admin.site.register(TestProject)
admin.site.register(TestCase)
admin.site.register(TestCaseStep, TestCaseStepAdmin)
