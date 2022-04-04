"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
"""

from django.db import models

class Loginteste(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    phoneno = models.IntegerField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'loginteste'


# Create your forms here.
"""
class NewUserForm(UserCreationForm):
	phoneno = forms.IntegerField(required=True)

	class Meta:
		model = User
		fields = ("username", "phoneno", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.phoneno = self.cleaned_data['phoneno']
		if commit:
			user.save()
		return user
"""
