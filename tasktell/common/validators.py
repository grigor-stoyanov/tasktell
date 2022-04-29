from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def only_letters_validator(value):
    if not value.isalpha():
        raise ValidationError(f'Name can only contain letters.')


@deconstructible
class FileMaxSizeValidator:
    BYTES_IN_MB = 1024

    def __init__(self, limit_mb):
        self.limit_mb = limit_mb * self.BYTES_IN_MB * self.BYTES_IN_MB

    def __call__(self, value):
        file_size = value.file.size
        if file_size > self.limit_mb:
            raise ValidationError(f"Max size of file is {self.limit_mb} MB")


@deconstructible
class MinDateValidator:
    def __init__(self, min_date):
        self.min_date = min_date

    def __call__(self, value):
        if value < self.min_date:
            raise ValidationError(f'Date must be greater than {self.min_date}')


@deconstructible
class MaxDateValidator:
    def __init__(self, max_date):
        self.min_date = max_date

    def __call__(self, value):
        if value > self.max_date:
            raise ValidationError(f'Date must be lesser than {self.max_date}')


@deconstructible
class UserExistsValidator:
    def __init__(self, users):
        self.users = users

    def __call__(self, email):
        for user in self.users:
            if email == user.profile.email:
                return
        raise ValidationError('Email does not match any active user.')
