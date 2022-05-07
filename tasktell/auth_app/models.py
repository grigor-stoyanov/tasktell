import datetime
from cloudinary.models import CloudinaryField
from django.contrib.auth import models as auth_models, get_user_model
from django.contrib.auth import base_user
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from tasktell.auth_app.managers import TasktellUserManager
from tasktell.common.validators import only_letters_validator, FileMaxSizeValidator, MinDateValidator


FIRST_NAME_MIN_LENGTH = 2
FIRST_NAME_MAX_LENGTH = 30
LAST_NAME_MIN_LENGTH = 2
LAST_NAME_MAX_LENGTH = 30
AVATAR_MAX_SIZE = 5
USERNAME_MAX_LENGTH = 16
GENDER_MALE = ('Male', 'Male')
GENDER_FEMALE = ('Female', 'Female')
GENDER_DO_NOT_SHOW = ('Do not show', 'Do not show')
GENDERS = [GENDER_FEMALE, GENDER_MALE, GENDER_DO_NOT_SHOW]
MIN_DATE = datetime.date(1935, 1, 1)


class TasktellUser(auth_models.PermissionsMixin, base_user.AbstractBaseUser):
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = TasktellUserManager()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            only_letters_validator,
        ),
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(LAST_NAME_MIN_LENGTH),
            only_letters_validator,
        )
    )
    # avatar = models.ImageField(
    #     upload_to='avatars/',
    #     blank=True, null=True,
    #     validators=(FileMaxSizeValidator(AVATAR_MAX_SIZE),))
    #

    avatar=CloudinaryField('image')

    birth_date = models.DateField(blank=True, null=True,
                                  validators=(MinDateValidator(MIN_DATE),)
                                  )
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        default=GENDER_DO_NOT_SHOW,
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True
    )

    class Meta:
        unique_together = ('email', 'user')


