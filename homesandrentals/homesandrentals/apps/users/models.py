from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
import os
import jwt


class UserManager(BaseUserManager):
    def create_user(self, username, email, phone, bio="", isActive=True, image="", password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            bio=bio,
            isActive=isActive,
            image=image
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(db_index=True, unique=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True, max_length=150)
    phone = models.CharField(db_index=True, unique=True, max_length=12)
    bio = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)
    image = models.URLField()

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now()+timedelta(days=60)
        token = jwt.encode(
            {'id': self.pk,
             'isActive': self.isActive,
             'exp': int(dt.strftime('%s'))
             },
            os.environ['APP_SECRET'],
            algorithm='HS256')

        return token.decode('utf-8')
