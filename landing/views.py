from django.shortcuts import render
from datetime import date
# Create your views here.

def home(request):
    today = date.today()
    return render(request, "landing/landing.html", {
        "name" : "José Horacio",
        "lastname" : "Ahuactzin",
        "age" : 21,
        "today" : today,
    })