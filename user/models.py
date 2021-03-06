from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class HxUserManager(BaseUserManager):
    def create_user(self, username, date_of_enter, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username.strip(),
            date_of_enter=date_of_enter,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, date_of_enter, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username.strip(),
            password=password,
            date_of_enter=date_of_enter,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class HxUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,

    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # 入职时间, 离职时间
    date_of_enter = models.DateField()
    date_of_leave = models.DateField(null=True, default=None)

    objects = HxUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_enter']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin