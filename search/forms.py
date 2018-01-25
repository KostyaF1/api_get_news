# -*- coding: utf-8 -*- 
from django import forms

class PostForm(forms.Form):
	search = forms.CharField()