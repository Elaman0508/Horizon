from django.db import models

class Rider(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='riders/')

    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.name


class Bike(models.Model):
    rider = models.OneToOneField(Rider, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='bikes/')

    def __str__(self):
        return f'{self.brand} {self.model}'


class Like(models.Model):
    rider = models.ForeignKey(Rider, related_name='likes', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rider', 'ip_address')
