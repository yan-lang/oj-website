import datetime
import os

from django.db import models
from mdeditor.fields import MDTextField

from account.models import User
from django.utils.translation import gettext as _

from website import settings


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
    LEXER_GRADER = 0
    PARSER_GRADER = 1
    SEMANTIC_GRADER = 2

    GRADER_CHOICES = [
        (LEXER_GRADER, "Lexer grader"),
        (PARSER_GRADER, "Parser grader"),
        (SEMANTIC_GRADER, "Semantic grader"),
    ]

    name = models.CharField(max_length=200,
                            help_text="Enter a assignment name.")

    description = MDTextField(blank=True,
                              help_text="Enter a description for your assignment.")

    grader = models.SmallIntegerField(choices=GRADER_CHOICES)

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


def submission_file_path(instance, filename):
    return '%s/protected/%s/%s/%s/%s' % (settings.MEDIA_ROOT, instance.user.pk,
                                         instance.assignment.pk, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
                                         filename)


class Submission(models.Model):
    SUBMITTED = 0
    GRADING = 1
    GRADED = 2

    STATUS_CHOICES = [
        (SUBMITTED, "Submitted"),
        (GRADING, "Grading"),
        (GRADED, "Graded")
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)

    submitted_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    # TODO: validate file size
    # Useful links (perhaps):
    # https://www.djangosnippets.org/snippets/1303/
    submitted_file = models.FileField(blank=True, upload_to=submission_file_path, max_length=300)

    status = models.SmallIntegerField(default=SUBMITTED, choices=STATUS_CHOICES)

    last_grade_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.assignment.__str__() + ": " + self.submitted_time.__str__()

    def submitted_file_name(self):
        return os.path.basename(self.submitted_file.name)


class GradeReport(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)

    # Sometimes, it might be ok to be passed even if the grade is 100%
    is_passed = models.BooleanField()

    # The grade of submission can be calculated from many GradeUnits
    # in a certain way.
    grade = models.IntegerField()
    total_grade = models.IntegerField(default=100)

    def __str__(self):
        return "{0} - {1}/{2}".format(self.submission, self.grade, self.total_grade)


class GradeUnit(models.Model):
    report = models.ForeignKey(GradeReport, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200)

    grade = models.IntegerField()
    total_grade = models.IntegerField(default=100)

    # Detailed grade report produced by grader.
    detail = models.TextField(blank=True)

    def __str__(self):
        return "{0} - {1}/{2}".format(self.name, self.grade, self.total_grade)
