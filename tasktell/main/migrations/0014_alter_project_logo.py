# Generated by Django 4.0.2 on 2022-04-25 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_tasks_is_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='media/project_logos/'),
        ),
    ]
