from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('coins', views.getCoins),
    path('mapData/<lat>/<long>/<query>', views.getMapData),
    path('getCards/<latitude>/<longitude>/<query>', views.getCardsForTransaction),
    path('dashboard/', views.getDashboard),
    path('sortedCards/', views.getSortedCards)
]
