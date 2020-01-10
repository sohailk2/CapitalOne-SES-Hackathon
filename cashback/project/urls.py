from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('home', views.home),
    path('coins', views.getCoins),
    path('mapData/<lat>/<long>/<query>', views.getMapData),
    path('getCards/<latitude>/<longitude>/<query>', views.getCardsForTransaction)
]
