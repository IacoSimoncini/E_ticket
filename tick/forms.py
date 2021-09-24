   
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from django import forms

from .models import Order, Event

class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ['num_ticket','immagine','category','nome','prezzo','luogo','data_evento']

class CreateUserForm(UserCreationForm):
		
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']