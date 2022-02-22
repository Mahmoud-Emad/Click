from typing import Any, Union

from django_countries.fields import CountryField
from django.contrib.auth.models import AnonymousUser, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.db import models

from server.jornal_app.models.abstracts import TimeStampedModel
from server.settings import LANGUAGE


def Get_progile_image_file_path(self, filename):
    """Handel user media files"""
    return f'server/media/users/{self.pk}/profile_images/{self.modified}{filename[filename.index("."):]}'

def Get_progile_cover_file_path(self, filename):
    """Handel user media files"""
    return f'server/media/users/{self.pk}/progile_covers/{self.modified}{filename[filename.index("."):]}'

def default_language():
    lang = dict(LANGUAGE['english'])
    return {'code': lang['code'], 'country': lang['country']}

class GenderChoice(models.TextChoices):
    MALE    = "MALE", "MALE"
    FEMALE  = "FEMALE", "FEMALE"
    OTHER   = "OTHER", "OTHER"

class MARITALSTATUS(models.TextChoices):
    SINGLE  = "SINGLE", "SINGLE"
    MARRIED = "MARRIED", "MARRIED"
    WIDOWED = "WIDOWED", "WIDOWED"
    DIVORCED = "DIVORCED", "DIVORCED"

class JornalBaseUserManger(BaseUserManager):

    def create_user(self, email : str, password:str) -> 'User':
        """Magic method to create user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email: str, password: str):
        ''' Create super user [admin] '''
        user = self.create_user(
            email                   = self.normalize_email(email),
            password                = password,
        )
        user.is_admin               = True
        user.is_superuser           = True
        user.is_staff               = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email           = models.EmailField(max_length=60, unique=True)
    username        = models.CharField(max_length=30, unique=True, null=True, blank=True)
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)
    
    last_login      = models.DateTimeField(auto_now = True)
    date_joined     = models.DateTimeField(auto_now = True)
    is_admin        = models.BooleanField(default = False)
    is_staff        = models.BooleanField(default = False)
    is_superuser    = models.BooleanField(default = False)
    is_active       = models.BooleanField(default = True)
    is_online       = models.BooleanField(default = False)

    objects         = JornalBaseUserManger()
    USERNAME_FIELD  = 'email'
    
    @property
    def full_name(self) -> str:
        """Normal method to concatonate f_name and l_name"""
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm : str , obj:Union[models.Model, AnonymousUser, None]=None) -> bool:
        """For checking permissions. to keep it simple all admin have ALL permissons"""
        return self.is_admin
    
    @staticmethod
    def has_module_perms(app_label : Any) -> bool:
        """Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)"""
        return True

    def save(self, *args : Any , **kwargs : Any) -> None:
        """Magic method to save user"""
        if not self.username:
            self.username = f'{self.first_name}_{self.id}'
        super().save(*args, **kwargs)

class UserProfile(User):
    profile_image = models.ImageField(upload_to = Get_progile_image_file_path) 
    profile_cover = models.ImageField(upload_to = Get_progile_cover_file_path)
    phone_nummber = models.CharField(default=None, max_length=15, unique=True, null=True)
    gender        = models.CharField(max_length=50, choices=GenderChoice.choices)
    marital_status= models.CharField(max_length=50, choices=MARITALSTATUS.choices)
    Bio           = models.TextField(max_length=580)
    country       = CountryField()
    city          = models.CharField(max_length=50)
    birthday      = models.DateField(auto_now=True)
    
    def __str__(self) -> isinstance:
        """Return string of instance"""
        return self.email


class UserUniversity(TimeStampedModel):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_uni')
    university    = models.CharField(max_length=50)
    from_date     = models.DateField(auto_now=True)
    to_date       = models.DateField(auto_now=True)
    i_still_study = models.BooleanField(default=False)

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return self.user.email


class UserSchool(TimeStampedModel):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sch')
    school        = models.CharField(max_length=50)
    from_date     = models.DateField(auto_now=True)
    to_date       = models.DateField(auto_now=True)
    i_still_study = models.BooleanField(default=False)

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return self.user.email


class UserWorkExperience(TimeStampedModel):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_work')
    company       = models.CharField(max_length=50)
    from_date     = models.DateField(auto_now=True)
    to_date       = models.DateField(auto_now=True)
    i_still_work  = models.BooleanField(default=False)

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return self.user.email


class UserSettings(TimeStampedModel):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_settings')
    other_messages  = models.BooleanField(default = True)
    online_status   = models.BooleanField(default = True)
    hide_email      = models.BooleanField(default = False)
    hide_friends    = models.BooleanField(default = False)
    look_account    = models.BooleanField(default = False)
    language        = models.JSONField(default = default_language)
    def __str__(self) -> isinstance:
        """Return string of instance"""
        return self.user.email