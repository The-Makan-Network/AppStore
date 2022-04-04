from django.db import models

class signingin(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'alluser'
