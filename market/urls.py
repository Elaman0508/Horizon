from django.urls import path
from . import views

urlpatterns = [
    path('', views.bike_market, name='bike_market'),
    path('<int:pk>/', views.bike_detail, name='bike_detail'),
    path('like/<int:pk>/', views.like_bike, name='like_bike'),
]
