from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.

    Handles user creation logic including regular users and superusers.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.

        Args:
            email (str): The user's email address.
            password (str, optional): The user's password.
            extra_fields (dict): Additional fields for the user model.

        Raises:
            ValueError: If no email is provided.

        Returns:
            CustomUser: The newly created user instance.
        """
        if not email:
            raise ValueError("E-Mail Adresse wird benötigt")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with administrative permissions.

        Args:
            email (str): The user's email address.
            password (str, optional): The user's password.
            extra_fields (dict): Additional fields for the user model.

        Returns:
            CustomUser: The newly created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of username.

    Fields:
        email (str): Unique email address used for authentication.
        is_active (bool): Indicates if the user account is active.
        is_staff (bool): Designates whether the user can log into the admin site.
        date_joined (datetime): Timestamp of when the user was created.
    """
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Return the string representation of the user.

        Returns:
            str: The user's email address.
        """
        return self.email
