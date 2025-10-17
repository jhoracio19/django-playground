from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Book
from django.db.models import Q


# Create your views here.

def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get("query_search")
        
        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)
            )

        return render(request, "minilibrary/minilibrary.html",{
            "books": books,
            "query": query
            
        })
    except Exception:
        return HttpResponseNotFound("Página no encontrada")