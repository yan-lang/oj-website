# Generated by Django 3.0.3 on 2020-04-01 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oj', '0008_auto_20200401_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Submitted'), (1, 'Grading'), (2, 'Graded')], default=0),
        ),
    ]