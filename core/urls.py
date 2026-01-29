from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),

    # Выезды команды
    path('rides/', views.ride_events, name='ride_events'),
    path('rides/<int:pk>/', views.ride_event_detail, name='ride_event_detail'),
]
