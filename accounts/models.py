from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.core.validators import RegexValidator
import random


class UserManager(BaseUserManager):
    #<-- The main method for creating all kind of Users-------------
    def create_user(self,email,user_name,phone_number, password =None, is_active = True, is_staff = False, is_admin = False, is_verified = False ):
        if not email:
            raise ValueError('User must have an email address')

        if not user_name:
            raise ValueError('User must have a username')

        if not phone_number:
            raise ValueError('User must have a phone number')
        user_obj = self.model(
            email = self.normalize_email(email),
            user_name = user_name,
            phone_number = phone_number,     
        )
    #   <------------Saving all fields Items here-------------->
        user_obj.set_password(password)
        user_obj.user_name = user_name
        user_obj.is_admin = is_admin
        user_obj.is_staff = is_staff
        user_obj.is_active = is_active
        user_obj.is_verified = is_verified

        user_obj.save(using = self._db)
        return user_obj

    def create_staffuser(self, email, user_name, password=None):
        user = self.create_user(
            email,
            user_name,
            password = password,
            is_staff = True
        )
        return user

    def create_superuser(self, email,user_name,phone_number, password = None):
        user = self.create_user(
            email,
            user_name,
            phone_number,
            password = password,
            is_admin = True,
            is_staff = True,
            is_verified = True,
        )
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length= 255, unique = True)
    user_name = models.CharField(max_length = 255, unique =  True)
    phone_reg = RegexValidator(regex=r'^\+?1?\d{9,15}$', message = "phone_number must be entered in the format: ' +99999999'. Up to 15 digits allowed")
    phone_number =  models.CharField(validators = [phone_reg], max_length = 16, unique=True)
    timestamp = models.DateTimeField(auto_now_add = True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number','user_name']

    objects = UserManager()

    def __str__(self):
        return self.user_name

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, perm, obj = None):
        return True

    #< --------- Still I'm confused with this two (  staff and admin and a little bit for active)--------->

    @property
    def staff(self):
        return self.is_staff

    @property
    def admin(self):
        return self.is_admin

    @property 
    def active(self):
        return self.is_active

class Code(models.Model):
    number = models.CharField(max_length=5, blank = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        super().save(*args, **kwargs)
