from django import forms
from .models import Loginteste

class Person(forms.ModelForm):
    class Meta:
        model = Loginteste
        fields = ['username', 'password']
