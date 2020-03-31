from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from oj.models import *


class AssignmentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ('name', 'create_date', 'deadline', 'course', 'alert')}),
        (_('Description'), {'fields': ('description',),
                            'classes': ('collapse',)}),
        (_('Auto grader'), {'fields': ('grader',)})
    )

    list_display = ('name', 'course', 'create_date', 'deadline')


class CourseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('identifier', 'name', 'description')}),
        (_('Registration'), {'fields': ('student',)}),
        (_('Date'), {'fields': ('create_date', 'update_date'),
                     'classes': ('collapse',)}),
    )

    filter_horizontal = ('student',)

    list_display = ('name', 'create_date', 'update_date')


class GradeUnitInline(admin.StackedInline):
    model = GradeUnit
    classes = ['collapse']
    extra = 0


class GradeReportAdmin(admin.ModelAdmin):
    model = GradeReport
    inlines = [GradeUnitInline]

    list_display = ('submission', 'grade', 'total_grade', 'is_passed')


class GradeReportInline(admin.StackedInline):
    model = GradeReport


class SubmissionAdmin(admin.ModelAdmin):
    inlines = [GradeReportInline]

    list_display = ('submitted_time', 'assignment', 'user')


admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Student)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(GradeReport, GradeReportAdmin)
admin.site.register(GradeUnit)
