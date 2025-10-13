from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    birt_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)
    genres = models.ManyToManyField(Genre, related_name="books")
    
    def __str__(self):
        return self.title

class BookDetail(models.Model):
    summary = models.TextField()
    cover_url = models.CharField()
    language = models.CharField()
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, related_name='detail')