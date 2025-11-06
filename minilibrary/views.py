from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Book, Review
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ReviewForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView
# Create your views here.

User = get_user_model()

class Hello(View):
    def get(self,request):
        return HttpResponse('Hola mundo desde CBV')

class WelcomeView(TemplateView):
    template_name = 'minilibrary/welcome.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = Book.objects.count()
        return context

class BookListView(ListView):
    model = Book
    template_name = 'minilibrary/book_list.html'
    context_object_name = 'books'
    paginate_by = 5
    
    

def index(request):
    try:
        books = Book.objects.all()
        
        # Sirven para traer la info de la URL (metodo GET)
        query = request.GET.get("query_search")
        date_start = request.GET.get("start")
        date_end = request.GET.get("end")
        
        # Los if son filtros
        
        # Filtro de libros por titulo o autor
        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)
            )
        
        # Filtro 
        if date_start and date_end:
            books = books.filter(publication_date__range=[
                date_start, date_end])
        
        paginator = Paginator(books, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        query_params = request.GET.copy()
        if "page" in query_params:
            query_params.pop("page")
        query_strings = query_params.urlencode()
        
        return render(request, "minilibrary/minilibrary.html",{
            "page_obj": page_obj,
            "query": query,
            "query_string": query_strings
            
        })
    except Exception:
        return HttpResponseNotFound("Página no encontrada")

def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            
            messages.success(request, "Gracias por la reseña")
            return redirect('recommend_book', book_id=book.id)
        else:
            messages.error(request, 'Corrige los errores del formulario','danger')
    return render(request, "minilibrary/add_review.html",{
        'form': form,
        'book': book
    } )