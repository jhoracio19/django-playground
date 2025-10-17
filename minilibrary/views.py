from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Book
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get("query_search")
        
        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)
            )
        
        paginator = Paginator(books, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        return render(request, "minilibrary/minilibrary.html",{
            "page_obj": page_obj,
            "query": query
            
        })
    except Exception:
        return HttpResponseNotFound("Página no encontrada")