from django import forms
from django.core.exceptions import ValidationError
from .models import *

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'categoryType',
           'postCategory',
           'title',
           'text',
       ]

   def clean(self):
       cleaned_data = super().clean()
       text = cleaned_data.get("text")
       title = cleaned_data.get("title")

       if text == title:
           raise ValidationError(
               "Описание не должно быть идентично названию."
           )

       return cleaned_data

# class PostForm(forms.Form):
#     title = forms.CharField(label='Title')
#     text = forms.CharField(label='Text')
#     author = forms.ModelChoiceField(label = 'Author', queryset=Author.objects.all())
#     categoryType = forms.ModelChoiceField(label = 'Category', queryset=Category.objects.all())
#     # categoryType.choices = forms.ModelChoiceField(label = 'Type Category', queryset=categoryType.choices)
