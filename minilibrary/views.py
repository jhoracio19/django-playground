from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Book


# Create your views here.

def index(request):
    try:
        books = Book.objects.all()
        author_id = request.GET.get('author')
        genre_id = request.GET.get('genre')
        
        if author_id:
            books = books.filter(author_id=author_id)
        
        if genre_id:
            books = books.filter(genres_id= genre_id)
        return render(request, "minilibrary/minilibrary.html",{
            'text' : "Hola desde la vista",
            'name' : 'HORACIO',
            'author' : author_id,
            'books' : books
        })
    except Exception:
        return HttpResponseNotFound("Página no encontrada")