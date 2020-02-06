from django.contrib import admin
from mdeditor.widgets import MDEditorWidget
from oj.models import *


class AssignmentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


admin.site.register(Course)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Student)
admin.site.register(Submission)
admin.site.register(GradeUnit)
