# Generated by Django 4.2.7 on 2024-01-18 17:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='class_file',
            field=models.FileField(blank=True, null=True, upload_to='course_files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'pptx'])]),
        ),
    ]
