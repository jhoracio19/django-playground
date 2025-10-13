from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loan
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

User = get_user_model()

class LoadInline(admin.TabularInline):
    model = Loan
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False
    verbose_name_plural = "Detalle del Libro"

class CustomUserAdmin(BaseUserAdmin):
    inlines= [LoadInline]
    list_display = ('username', 'email')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, BookDetailInline]
    list_display = ('title', 'author', 'pages', 'publication_date')
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'genres', 'publication_date')
    ordering = ['-publication_date']
    date_hierarchy = 'publication_date'

admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Loan)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)