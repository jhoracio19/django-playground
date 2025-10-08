from django.shortcuts import render
from datetime import date
# Create your views here.

def home(request):
    today = date.today()
    stack = ['Python', 'JavaScript', 'PHP', 'Django', 'Golang']
    return render(request, "landing/landing.html", {
        "name" : "Horacio",
        "lastname" : "Ahuactzin",
        "age" : 21,
        "today" : today,
        "stack" : stack 
    })