from django.db import models

class Allusers(models.Model):
  username = models.CharField(unique=True, max_length=16)
  phoneno = models.BigIntegerField(primary_key=True)
  password = models.CharField(max_length=12)
  
  class Meta:
    managed = True
    db_table = 'allusers'
