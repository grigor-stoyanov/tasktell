# Generated by Django 4.0.2 on 2022-04-25 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='messages',
        ),
        migrations.AddField(
            model_name='chat',
            name='messages',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='chat.messages'),
            preserve_default=False,
        ),
    ]
