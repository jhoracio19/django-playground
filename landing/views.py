from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
# Create your views here.

def home(request):
    today = date.today()
    stack = [
            {'id' : 'python', 'name' : 'Python'},
            {'id' : 'javascript', 'name' : 'JavaScript'}, 
            {'id' : 'php', 'name' : 'PHP'}, 
            {'id' : 'django', 'name' : 'Django'}, 
            {'id' : 'go', 'name' : 'Go'}
            ]
    
    return render(request, "landing/landing.html", {
        "name" : "Horacio",
        "lastname" : "Ahuactzin",
        "age" : 21,
        "today" : today,
        "stack" : stack 
    })

def stack_detail(request, tool):
    return HttpResponse(f"Tecnología: {tool}")