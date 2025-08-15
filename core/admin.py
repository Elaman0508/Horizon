from django.contrib import admin
from .models import Rider, Bike, Like
from .models import ForSaleBike, BikePhoto

class BikePhotoInline(admin.TabularInline):
    model = BikePhoto
    extra = 1
    max_num = 10  # до 10 фото
    fields = ['image']

@admin.register(ForSaleBike)
class ForSaleBikeAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'type')
    inlines = [BikePhotoInline]



@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ('name', 'likes_count')

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('rider', 'brand', 'model')
