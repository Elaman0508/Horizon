from django.contrib import admin
from .models import ForSaleBike, BikePhoto, RideEvent, RidePhoto, EventComment, Like

# ----------------------------------------
# Фото для велосипеда
# ----------------------------------------
class BikePhotoInline(admin.TabularInline):
    model = BikePhoto
    extra = 1
    max_num = 10
    fields = ['image']

# ----------------------------------------
# Велосипеды
# ----------------------------------------
@admin.register(ForSaleBike)
class ForSaleBikeAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'type', 'price', 'contact', 'created_at')
    list_filter = ('type', 'brand')
    search_fields = ('title', 'brand')
    inlines = [BikePhotoInline]

# ----------------------------------------
# Лайки велосипедов
# ----------------------------------------
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('bike', 'ip_address', 'created_at')
    list_filter = ('bike', 'created_at')
    search_fields = ('ip_address',)

# ----------------------------------------
# Фото для выездов
# ----------------------------------------
class RidePhotoInline(admin.TabularInline):
    model = RidePhoto
    extra = 1
    max_num = 10
    fields = ['image']

# ----------------------------------------
# Выезды команды
# ----------------------------------------
@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'event_time', 'location', 'created_at')
    list_filter = ('event_date', 'location')
    search_fields = ('title', 'location')
    inlines = [RidePhotoInline]

# ----------------------------------------
# Комментарии к выездам
# ----------------------------------------
@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ('event', 'author_ip', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author_ip', 'content')
