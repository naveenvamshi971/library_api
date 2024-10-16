from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book  

# Register your models here.

@admin.register(Book)  # Register the Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn', 'pages', 'language')  # Customize displayed fields
    search_fields = ('title', 'author')  # Add search functionality


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role',)

admin.site.register(User, CustomUserAdmin)
