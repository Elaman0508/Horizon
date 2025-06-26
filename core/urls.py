from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rider/<int:pk>/', views.rider_detail, name='rider_detail'),
    path('like/<int:pk>/', views.like_rider, name='like_rider'),
    path('bikes/', views.bike_rating, name='bike_rating'),
]
