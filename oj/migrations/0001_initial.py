# Generated by Django 3.0.3 on 2020-02-06 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a assignment name.', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a description for your assignment.')),
                ('deadline', models.DateTimeField()),
                ('grader', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a course name (e.g. Math, Chinese).', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a description for your course.')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_passed', models.BooleanField()),
                ('submited_time', models.DateTimeField(auto_now=True)),
                ('submited_file', models.FilePathField()),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='oj.Assignment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(help_text='Enter your student ID.', max_length=20)),
                ('name', models.CharField(help_text='Enter your real name.', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GradeUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('grade', models.IntegerField()),
                ('total_grade', models.IntegerField(default=100)),
                ('grade_report', models.TextField()),
                ('submission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='oj.Submission')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='oj.Course'),
        ),
    ]
