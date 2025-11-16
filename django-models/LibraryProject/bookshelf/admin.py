# bookshelf/admin.py
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # columns shown in the list page
    list_display = ("title", "author", "publication_year")

    # quick filters in the right sidebar
    list_filter = ("publication_year", "author")

    # search box - searches these fields (partial matches)
    search_fields = ("title", "author")

    # make title the clickable link to the change page
    list_display_links = ("title",)

    # allow inline editing of publication_year in the list view
    # (note: list_editable cannot include the same field as list_display_links)
    list_editable = ("publication_year",)

    # optional conveniences
    ordering = ("title",)
    list_per_page = 20