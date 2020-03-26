from django import forms
from .models import *


class SucriberForm(forms.ModelForm):
    class Meta:
        model = Sucriber
        fields = ['name', 'email']