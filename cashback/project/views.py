from django.http import HttpResponse
from django.shortcuts import render
import firebase

# firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)

def home(request):
    return render(request, 'project/home.html')

def firebase_test():
    pass
    # data.get("restart", "name")
    # data.put('restart', 'triggeredPressed', False)