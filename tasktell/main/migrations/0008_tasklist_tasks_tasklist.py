# Generated by Django 4.0.2 on 2022-04-09 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_tasks_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='tasks',
            name='tasklist',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.tasklist'),
            preserve_default=False,
        ),
    ]
