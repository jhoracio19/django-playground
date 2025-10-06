from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
# Create your views here.

days_of_week = {
    "monday" : "Pienso luego existo",
    "tuesday" : "La vida es un sueño",
    "wednesday" : "El conocimiento es poder",
    "thursday" : "Se el cambio que quieras ver en el mundo",
    "friday" : "Solo se que no se nada",
    "saturday" : "Vive con si fuera el ultimo dia",
    "sunday" : "Da un poquito mas, todos los dias",
}

def days_week_with_number(request, day):
    days = list(days_of_week.keys())
    if day > len(days):
        return HttpResponseNotFound("El día no existe.")
    redirect_day= days[day-1]
    return HttpResponseRedirect(f"/quotes/{redirect_day}")
    

def days_week(request, day):
    try:
        quote_text = days_of_week[day]
        return HttpResponse(quote_text)
    except:
        return HttpResponseNotFound("Este día no existe.")