from django.contrib import admin
from django.contrib.auth import get_user_model

from tasktell.auth_app.models import Profile

UserModel = get_user_model()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'description')


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
