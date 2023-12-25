from django.forms import ModelForm
from .models import Todo

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']

# yourapp/forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

