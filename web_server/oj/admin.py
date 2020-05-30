import csv

from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.http import HttpResponse
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
        (None, {'fields': ('identifier', 'name', 'description', 'detail_description')}),
        (_('Registration'), {'fields': ('student',)}),
        (_('Date'), {'fields': ('create_date', 'update_date')}),
    )

    filter_horizontal = ('student',)

    list_display = ('name', 'create_date', 'update_date')

    actions = ['export_grade']

    def export_grade(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="grades.csv"'
        writer = csv.writer(response)

        courses = queryset
        for course in courses:
            # 1. get all assignment of the course
            assignments = Assignment.objects.filter(course=course)

            # 2. print header
            # email, actual_name, student_id, assignment1, grade, assignment2, grade, ...
            header = ['email', 'name', 'student_id', ]
            for assignment in assignments:
                header += [assignment.name]
            writer.writerow(header)

            # 3. get all students of the course
            users = course.student.all()
            for user in users:
                try:
                    student = user.student
                except FieldDoesNotExist:
                    continue

                data = [user.email, student.name, student.student_id]
                for assignment in assignments:
                    submission = Submission.objects.filter(assignment=assignment).filter(user=user) \
                        .order_by('gradereport__grade').reverse()
                    if submission.exists():
                        data += [submission.first().gradereport.grade]
                    else:
                        data += [0]
                writer.writerow(data)

        return response

    export_grade.short_description = 'export grade'


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


class StudentAdmin(admin.ModelAdmin):
    model = Student

    list_display = ('user', 'student_id', 'name')


admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(GradeReport, GradeReportAdmin)
admin.site.register(GradeUnit)
