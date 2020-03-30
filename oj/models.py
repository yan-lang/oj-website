from django.db import models
from mdeditor.fields import MDTextField

from account.models import User
from django.utils.translation import gettext as _


class Course(models.Model):
    identifier = models.SlugField(max_length=100, help_text=_("Will be used in course home page url"), unique=True)

    name = models.CharField(max_length=200,
                            help_text=_("Enter a course name (e.g. Math, Chinese)."))

    description = models.TextField(blank=True,
                                   help_text=_("Enter a description for your course."))

    # --  Dates --
    create_date = models.DateTimeField(blank=True)
    update_date = models.DateTimeField(blank=True)

    # -- Foreign key --
    student = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a assignment name.")

    description = MDTextField(blank=True,
                              help_text="Enter a description for your assignment.")

    grader = models.FileField(blank=True)

    alert = models.TextField(blank=True, help_text=_("If you have any news to remind students, please enter here."))

    # --  Dates --
    create_date = models.DateTimeField(blank=True)
    deadline = models.DateTimeField()

    # -- Foreign key --
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    student_id = models.CharField(max_length=20, help_text="Enter your student ID.",
                                  blank=True)
    name = models.CharField(max_length=100, help_text="Enter your real name.",
                            blank=True)

    def __str__(self):
        return "Student " + self.user.__str__()


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)

    # Sometimes, it might be ok to be passed even if the grade is 100%
    is_passed = models.BooleanField()

    # The grade of submission can be calculated from many GradeUnits
    # in a certain way.
    grade = models.IntegerField()
    total_grade = models.IntegerField(default=100)

    submited_time = models.DateTimeField()

    # TODO: validate file size
    # Useful links (perhaps):
    # https://www.djangosnippets.org/snippets/1303/
    submited_file = models.FileField(blank=True)

    def __str__(self):
        return self.assignment.__str__() + ": " + self.submited_time.__str__()


class GradeUnit(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200)

    grade = models.IntegerField()
    total_grade = models.IntegerField(default=100)

    # Detailed grade report produced by grader.
    grade_report = models.TextField(blank=True)

    def __str__(self):
        return self.name
