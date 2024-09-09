from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure the superuser has all required fields
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()

    class Role(models.TextChoices):
        STUDENT = 'St', 'Student'
        TEACHER = 'Tr', 'Teacher'
    username = models.CharField(max_length=150, unique=True, null=True)
    email = models.CharField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True)
    second_name = models.CharField(max_length=50, null=True)
    phone = PhoneNumberField(blank=True, region="RU", null=True)
    password = models.CharField(max_length=255)

    grade_level = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.STUDENT,
        null=True
    )
    lessons = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

