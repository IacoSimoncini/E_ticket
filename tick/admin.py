from django.contrib import admin
from .models import Tick, Event

# Register your models here.
admin.site.register(Tick)
admin.site.register(Event)