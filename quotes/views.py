from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
# Create your views here.


def days_week(request, day):
    quote_text = None
    if day == 'monday':
        quote_text = "Pienso, luego existo"
    elif day == 'tuesday':
        quote_text = "La vida es un sueño"
    else:
        return HttpResponseNotFound("No hay frase para este día")
    
    return HttpResponse(quote_text )