from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage_view, name = 'MainPage'),
    path('menciones', views.menciones_view, name = 'Menciones'),
    path('hashtags', views.hashtags_view, name = 'Hashtags'),
    path('sentimientos', views.sentimientos_view, name = 'Sentimientos'),
    path('ayuda', views.ayuda, name = 'Ayuda'),
]