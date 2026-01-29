from django.db import models

# ----------------------------------------
# Велосипеды на продажу
# ----------------------------------------
BIKE_TYPES = [
    ('road', 'Шоссейный'),
    ('mtb', 'Горный'),
    ('bmx', 'BMX'),
    ('city', 'Городской'),
    ('fixie', 'Фикс'),
    ('other', 'Другой'),
]

class ForSaleBike(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=BIKE_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ----------------------------------------
# Фото для велосипеда
# ----------------------------------------
class BikePhoto(models.Model):
    bike = models.ForeignKey(ForSaleBike, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bikes/photos/')

    def __str__(self):
        return f"Фото {self.bike.title}"

# ----------------------------------------
# Лайки для велосипедов
# ----------------------------------------
class Like(models.Model):
    bike = models.ForeignKey(ForSaleBike, related_name='likes', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('bike', 'ip_address')

    def __str__(self):
        return f"Лайк {self.bike.title} от {self.ip_address}"

# ----------------------------------------
# Выезды команды
# ----------------------------------------
class RideEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    event_date = models.DateField()   # дата события
    event_time = models.TimeField()   # время события
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ----------------------------------------
# Фото для выездов
# ----------------------------------------
class RidePhoto(models.Model):
    event = models.ForeignKey(RideEvent, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rides/photos/')

    def __str__(self):
        return f"Фото {self.event.title}"


class EventComment(models.Model):
    event = models.ForeignKey(RideEvent, related_name='comments', on_delete=models.CASCADE)
    author_ip = models.GenericIPAddressField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий к {self.event.title}"



class BikeImage(models.Model):
    bike = models.ForeignKey(
        ForSaleBike,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='bikes/')
