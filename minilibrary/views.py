from django.db.models.query import QuerySet
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
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import time
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

class BookDetailView(DeleteView):
    model = Book
    template_name = "minilibrary/book_detail.html"
    context_object_name = "book"

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'minilibrary/add_review.html'
    
    def form_valid(self, form):
        book_id = self.kwargs.get('pk')
        book = Book.objects.get(pk=book_id)
        form.instance.book = book
        form.instance.user_id = 1
        messages.success(self.request, "Gracias por tu reseña.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('book_detail',kwargs={'pk': self.kwargs.get('pk')})

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'minilibrary/add_review.html'
    
    def get_queryset(self):
        return Review.objects.filter(user_id=1)
    
    def form_valid(self, form):    
        messages.success(self.request, "Se ha actualizado tu reseña, correctamente.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al guardar los datos")
    
    def get_success_url(self):
        review = Review.objects.get(pk=self.kwargs.get('pk'))
        book_id = review.book.id
        return reverse_lazy('book_detail',kwargs={'pk': book_id})

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'minilibrary/review_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    
    def get_queryset(self):
        return Review.objects.filter(user_id=1)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Tu reseña fue eliminada.")
        return super().delete(request, *args, **kwargs)

def home(request):
    print(request.user)
    return HttpResponse("Hola")

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
    

def time_test(request):
    time.sleep(2)
    return HttpResponse('Esta vista tardo 2 segundos')