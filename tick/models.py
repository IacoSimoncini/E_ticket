from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django import forms
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

from eth_typing.evm import Address
# Create your models here.
class Tick(models.Model):
    immagine = models.ImageField()
    nome = models.CharField(max_length=100)
    prezzo = models.FloatField()

    def __str__(self):
        return self.nome

@property
def image_url(self):
    if self.immagine and hasattr(self.immagine, 'url'):
        return self.immagine.url

class Event(models.Model):
    CATEGORY = (
		('Cinema', 'Cinema'),
		('Teatro', 'Teatro'),
		('Sport', 'Sport'),
		('Concerti', 'Concerti'),
		)

    num_ticket = models.IntegerField() #ticket disponibili
    immagine = models.ImageField(null=True, blank=True, default='static/tick/default.jpg')
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    nome = models.CharField(max_length=100)
    prezzo = models.FloatField()
    luogo = models.CharField(max_length=100)
    data_evento = models.DateTimeField()
    #data_evento=models.CharField(max_length=100, default="10 marzo")
    address= models.CharField(max_length=100,default=0)
    def __str__(self):
        return self.nome
	

class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.product.name


