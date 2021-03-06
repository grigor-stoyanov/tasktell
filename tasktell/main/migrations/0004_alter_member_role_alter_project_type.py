# Generated by Django 4.0.2 on 2022-04-08 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_member_role_alter_member_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(choices=[('Owner', 'OWNER'), ('Moderator', 'MODERATOR'), ('Member', 'MEMBER'), ('Applicant', 'APPLICANT')], max_length=10),
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('Private', 'Private'), ('Public', 'Public')], default=('Public', 'Public'), max_length=10),
        ),
    ]
