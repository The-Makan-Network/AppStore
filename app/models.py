from django.db import models

class useraccounts(models.Model):
  username = models.TextField(null=True)
  phoneno = models.IntegerField(null=True)
  password = models.TextField(null=True)
