from django.db import models
from mdeditor.fields import MDTextField

from account.models import User


class Course(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a course name (e.g. Math, Chinese).")
    description = models.TextField(blank=True,
                                   help_text="Enter a description for your course.")

    def __str__(self):
        return self.name


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200,
                            help_text="Enter a assignment name.")

    description = MDTextField(blank=True,
                              help_text="Enter a description for your assignment.")

    deadline = models.DateTimeField()

    grader = models.FileField(blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, help_text="Enter your student ID.")
    name = models.CharField(max_length=100, help_text="Enter your real name.")

    def __str__(self):
        return self.user.__str__()


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
    # Userful links (perhaps):
    # https://www.djangosnippets.org/snippets/1303/
    submited_file = models.FileField(blank=True)

    def __str__(self):
        return self.assignment.__str__() + ": " + self.submited_time.__str__()


class GradeUnit(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200)

    grade = models.IntegerField()
    total_grade = models.IntegerField(default=100)

    # Detailed grade report produeced by grader.
    grade_report = models.TextField(blank=True)

    def __str__(self):
        return self.name
