# Generated by Django 3.0.3 on 2020-03-30 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oj', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='submited_file',
            new_name='submitted_file',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='submited_time',
            new_name='submitted_time',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='is_passed',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='total_grade',
        ),
        migrations.CreateModel(
            name='GradeReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_passed', models.BooleanField()),
                ('grade', models.IntegerField()),
                ('total_grade', models.IntegerField(default=100)),
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='oj.Submission')),
            ],
        ),
        migrations.AlterField(
            model_name='gradeunit',
            name='submission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='oj.GradeReport'),
        ),
    ]
