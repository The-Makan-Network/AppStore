from django.db import models
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    email = models.EmailField()
    balance = models.DecimalField(max_digits=6, decimal_places=2)
    firstname = models.CharField(max_length=56)
    lastname = models.CharField(max_length=45)
    cellphone = models.CharField(max_length=14)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=45)
    post_code = models.CharField(max_length=45)
    country = models.CharField(max_length=45)

class Product(models.Model):