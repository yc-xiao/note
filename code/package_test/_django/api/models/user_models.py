from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

# 用户继承AbstractBaseUser，对比Abstractser补充方法去掉多余字段
# 用户密码修改待处理
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, help_text='用户账号')
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False, help_text='是否是adminsite的管理员')
    is_active = models.BooleanField(default=True, help_text='账号是否可用')
    created_time = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    # REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = '用户表'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def save(self, *args, **kw):
    #     if not getattr(self, 'id'):
    #         self.set_password(self.password)
    #     return super(User, self).save(*args, **kw)
