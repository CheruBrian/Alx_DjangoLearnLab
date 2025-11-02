from django.contrib import admin
from .models import Book

#customization of admin interface for Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  
    search_fields = ('title', 'author')                    
    list_filter = ('publication_year',) 

# register the Book model with the customized admin
admin.site.register(Book, BookAdmin)
