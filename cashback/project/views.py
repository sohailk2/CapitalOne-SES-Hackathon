from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import project.suggestion as Suggestion
import project.map as Map
import time

user = "Alice"

def home(request):

# Query, long, lat => mapData  127.800./mapData
# response

    if request.method == 'POST':
        print("POST", request.POST)
        return redirect('/mapData')

    # print(Suggestion.monthToQuarter(12))

    db = firestore.client()

    users_ref = db.collection(u'cards')
    docs = users_ref.stream()

    total = ""

    for doc in docs:
        total += u'{} => {}'.format(doc.id, doc.to_dict())

    return render(request, 'project/index.html', {"total":total})

def getCoins(request):
    return JsonResponse({'coins':int(round(time.time() * 1000))})

def getMapData(request, lat, long, query):
    #send back map data for things to plot
    print("in get map data")
    return JsonResponse({'lat': lat, 'long': long, 'query': query});

    # if (request.method == 'POST'):
    #     query = request.POST.get("query")
    #     latitude = request.POST.get("latitude")
    #     longitude = request.POST.get("longitude")
    #     print(query, latitude, longitude)
    #     return JsonResponse({'post': int(round(time.time() * 1000))});
    # return JsonResponse({'get':int(round(time.time() * 1000))});



def getCardsForTransaction(request, latitude, longitude, query):
    # so get a list of sorted cards for category
    # so get the category from latitude and longitude

    places =  Map.getStoreType('{},{}'.format(latitude,longitude), query)

    category = list(map(Map.getTypes,places))[0]
    print(places)

    cards = Suggestion.bestCard(category, user)
    return JsonResponse({'cards':cards, 'name': places[0]['name']});

def getDashboard(request):



    return render(request, 'project/dashboard.html')

def getSortedCards(request):
    sortedCards = Suggestion.newCard(user)
    return JsonResponse({'cards': sortedCards})


