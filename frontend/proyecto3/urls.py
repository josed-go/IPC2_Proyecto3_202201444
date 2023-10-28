from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage_view, name = 'MainPage'),
    path('menciones', views.menciones_view, name = 'Menciones'),
    path('hashtags', views.mainpage_view, name = 'Hashtags'),
    path('sentimientos', views.mainpage_view, name = 'Sentimientos'),
    path('graficas', views.mainpage_view, name = 'Graficas'),
    path('ayuda', views.ayuda, name = 'Ayuda'),
]