from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from django import forms

from .models import Customer, Order, Event

class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ['num_ticket','immagine','category','nome','prezzo','luogo','data_evento']

class CreateUserForm(ModelForm):
	
	class Meta:
		model = Customer
		fields = ['username', 'email', 'password1', 'password2']

