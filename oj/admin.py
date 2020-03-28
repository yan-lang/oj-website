from django.contrib import admin
from mdeditor.widgets import MDEditorWidget
from oj.models import *
from django.utils.translation import gettext, gettext_lazy as _


class AssignmentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ('name', 'create_date', 'deadline', 'course', 'alert')}),
        (_('Description'), {'fields': ('description',),
                            'classes': ('collapse',)}),
        (_('Auto grader'), {'fields': ('grader',)})
    )


class CourseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('identifier', 'name', 'description')}),
        (_('Registration'), {'fields': ('student',)}),
        (_('Date'), {'fields': ('create_date', 'update_date'),
                     'classes': ('collapse',)}),
    )

    filter_horizontal = ('student',)

    list_display = ('name', 'create_date', 'update_date')


admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Student)
admin.site.register(Submission)
admin.site.register(GradeUnit)
