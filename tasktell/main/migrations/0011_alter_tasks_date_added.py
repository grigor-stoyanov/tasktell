# Generated by Django 4.0.2 on 2022-04-12 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_tasklist_tasks_tasks_task_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='date_added',
            field=models.DateField(auto_now=True),
        ),
    ]