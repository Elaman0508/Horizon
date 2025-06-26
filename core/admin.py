from django.contrib import admin
from .models import Rider, Bike, Like

@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ('name', 'likes_count')

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('rider', 'brand', 'model')
