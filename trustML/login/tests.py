from django.test import TestCase
from django.utils import timezone
from .models import MyUserManager, User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from django.test import Client

def create_user(t_email, t_password):
    return User.objects.create(email=t_email, password=t_password)

class test_userinformation(TestCase):
    #test user model
    def test_staff(self):
        newuser = create_user('jam233@jam233.com','11aaBB!!')
        self.assertIs(newuser.is_staff, False)

    def test_active(self):
        newuser = User(email='jam233@jam233.com')
        self.assertIs(newuser.is_active, True)

    def test_create(self):
        newuser = User(email='jam233.com')
        self.assertIs(newuser.is_active, True)

    def test_description(self):
        newusera = create_user('jam233@jam233.com','11aaBB!!')
        newuserb = create_user('jam2333@jam2333.com','11aaBB!!')
        self.assertIs(str(newusera.description), str(newuserb.description))

    def test_description(self):
        newusera = create_user('jam233@jam233.com','11aaBB!!')
        newuserb = create_user('jam2333@jam2333.com','11aaBB!!!')
        self.assertIs((newusera.password == newuserb.password),False)
    #test functions in data model
    def test_getfullname(self):
        newusera = create_user('jam233@jam233.com','11aaBB!!')
        newuserb = create_user('jam2333@jam2333.com','11aaBB!!!')
        self.assertIs((newusera.get_full_name() == newuserb.get_full_name()),False)

    def test_getshortname(self):
        newusera = create_user('jam233@jam233.com','11aaBB!!')
        newuserb = create_user('jam2333@jam2333.com','11aaBB!!!')
        self.assertIs((newusera.get_short_name() == newuserb.get_short_name()),False)
    #test interface for blockchain
    def test_bcacc(self):
        newusera = create_user('jam233@jam233.com','11aaBB!!')
        newuserb = create_user('jam2333@jam2333.com','11aaBB!!!')
        newusera.setAddress('1')
        newuserb.setAddress('2')
        self.assertIs((newusera.get_bc_acc() == newuserb.get_bc_acc()),False)

    def test_setaddress(self):
        newusera = create_user('jam233@jam233.com','11aaBB!!')
        newusera.setAddress('1')
        self.assertIs((newusera.wallet_address == '1'),True)

    def test_createac(self):
        newusera = create_user('jam233@jam233.com','11aaBB!!')
        newuserb = create_user('jam2333@jam2333.com','11aaBB!!!')
        newusera.create_bc_acc("str")
        newuserb.create_bc_acc("strr")
        self.assertIs((newusera.get_bc_acc() == newuserb.get_bc_acc()),False)

    def test_balance(self):
        newusera = create_user('jam233@jam233.com','11aaBB!!')
        newuserb = create_user('jam2333@jam2333.com','11aaBB!!!')
        newusera.create_bc_acc("str")
        newuserb.create_bc_acc("strr")
        self.assertIs((newusera.get_bc_acc() == newuserb.get_bc_acc()),False)
    #test the Django login and register status
    def test_login(self):
        c = Client()
        response = c.post('', {'Email': 'john', 'password': '11aaBB!!'})
        self.assertIs(response.status_code, 200)

    def test_register(self):
         c = Client()
         response = c.post('/signup/', {'Email': 'john', 'Password': '11aaBB!!','Passwordconformation':'11aaBB!!'})
         self.assertIs(response.status_code, 200)
