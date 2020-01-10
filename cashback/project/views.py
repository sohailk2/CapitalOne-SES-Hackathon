from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import project.suggestion as Suggestion
import time



data = os.path.join(os.path.dirname(__file__), '../project/firestore.json')
cred = credentials.Certificate(data)

# Use the application default credentials
firebase_admin.initialize_app(cred, {
  'projectId': 'ses-hackathon-c6cf5',
})



def home(request):
    print(Suggestion.monthToQuarter(12))

    db = firestore.client()

    users_ref = db.collection(u'cards')
    docs = users_ref.stream()

    total = ""

    for doc in docs:
        total += u'{} => {}'.format(doc.id, doc.to_dict())

    return render(request, 'project/home.html', {"total":total})

def getCoins(request):
    return JsonResponse({'coins':int(round(time.time() * 1000))})