from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
import os
import sys
sys.path.append(os.path.abspath(os.path.join('..', 'trustML')))
from trustML.compile_solidity_utils import w3
from django.core.validators import int_list_validator

def countNormalUsers():
    users = User.objects.all()
    count_normal = len(users)
    for u in users:
        if(u.is_superuser):
            count_normal-=1
    return count_normal


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if extra_fields.get('is_superuser') is  True:
            user.setAddress(w3.eth.accounts[0])
        else:
            count_normal = countNormalUsers()
            print(count_normal%10+1)
            user.setAddress(w3.eth.accounts[count_normal%10+1])
        user.save()
        return user

    def create_buyer(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_buyer = True
        if extra_fields.get('is_superuser') is  True:
            user.setAddress(w3.eth.accounts[0])
        else:
            count_normal = countNormalUsers()
            print(count_normal%10+1)
            user.setAddress(w3.eth.accounts[count_normal%10+1])
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        print("Creating Superuser In Login View.py")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('wallet_address', w3.eth.accounts[1])
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    # w3.eth.accounts[self.pk]

    wallet_address = models.CharField(max_length=42, default= w3.personal.newAccount("test"))

    image = models.ImageField(
        upload_to='user_photo/',
        blank=True,
    )
    cover = models.ImageField(
        upload_to='user_photo/',
        blank=True,
    )
    description = models.CharField(
        max_length=1000,
        default='Add a short description of yourself.'
    )
    is_staff = models.BooleanField(
        'I want to be a model provider',
        default=False,
        help_text='Is the user allowed to have access to the admin',
    )
    is_buyer = models.BooleanField(
        'I want to be a buyer',
        default=False,
        help_text='Is the user allowed to have access to be a buyer',
    )

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text= 'Is the user account currently active',
    )
    bought_model = models.CharField(validators=[int_list_validator],max_length=10000,default="")
    # bought_model = models.CharField(validators=[int_list_validator],max_length=10000,null = True)
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['wallet_address']
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        short_name = ''
        for c in self.email:
            if c == '@':
                break
            short_name += c
        return short_name

    def get_is_staff(self):
        return self.is_staff
    
    def get_is_buyer(self):
        return self.is_buyer

    def get_bc_acc(self):
        return self.wallet_address

    def get_balance(self):
        return w3.fromWei(w3.eth.getBalance(w3.toChecksumAddress(self.wallet_address)), 'ether')

    def create_bc_acc(self, passphrase):
        self.wallet_address = models.CharField(max_length=42, default=w3.personal.newAccount(passphrase))

    def setAddress(self, address):
        self.wallet_address = address
