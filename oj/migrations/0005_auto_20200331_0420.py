# Generated by Django 3.0.3 on 2020-03-31 04:20

from django.db import migrations, models
import oj.models


class Migration(migrations.Migration):

    dependencies = [
        ('oj', '0004_auto_20200331_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submitted_file',
            field=models.FileField(blank=True, max_length=300, upload_to=oj.models.submission_file_path),
        ),
    ]