from django.db import models
from django.contrib.auth.models import User
import datetime
from django import forms

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
    #data = models.DateField(auto_now_add=True, null=True)
    data_evento=models.CharField(max_length=100, default="10 marzo")
    address= models.CharField(max_length=100,default=0)
    def __str__(self):
        return self.nome
	

class Customer(models.Model):
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)
	user = models.CharField(max_length=100)
	address = models.CharField(max_length=43, null=True, default='')		# cambiare null=False in futuro

	def __str__(self):
		return self.name

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

	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.product.name


