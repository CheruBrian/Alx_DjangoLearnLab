from django.contrib import admin
from .models import Book
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

#customization of admin interface for Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  
    search_fields = ('title', 'author')                    
    list_filter = ('publication_year',) 

# register the Book model with the customized admin
admin.site.register(Book, BookAdmin)

class CustomUserAdmin(UserAdmin):
    # Display these fields in the admin user list
    list_display = ("username", "email", "date_of_birth", "is_staff")

    # Add date_of_birth and profile_photo to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
admin.site.register(CustomUser, CustomUserAdmin)