from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.backends import BaseBackend
from . import extras
# part 2
from django_cryptography.fields import encrypt

# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=97)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

class OurBackend(BaseBackend):
    def authenticate(self, request, username, password):
        assert(None not in [username, password])
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        pwrd_valid = extras.check_password(user, password)
        if pwrd_valid:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    # part 2
    product_name = encrypt(models.CharField(max_length=50, unique=True))
    product_image_path = encrypt(models.CharField(max_length=100, unique=True))
    recommended_price = encrypt(models.IntegerField())
    description = encrypt(models.CharField(max_length=250))

class Card(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.BinaryField(unique=True)
    product = models.ForeignKey('LegacySite.Product', on_delete=models.CASCADE, default=None)
    # part 2
    amount = encrypt(models.IntegerField())
    fp = encrypt(models.CharField(max_length=100, unique=True))
    user = models.ForeignKey('LegacySite.User', on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
