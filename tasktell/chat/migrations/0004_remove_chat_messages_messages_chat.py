# Generated by Django 4.0.2 on 2022-04-25 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chat_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='messages',
        ),
        migrations.AddField(
            model_name='messages',
            name='chat',
            field=models.ManyToManyField(to='chat.Chat'),
        ),
    ]