from django.db import models

class Loginteste(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    phoneno = models.IntegerField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'allusers'
