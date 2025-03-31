from django.contrib import admin
from django.utils.html import format_html
from .models import Book  # Import Book model

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author', 'price', 'cover_preview','quantity','return_due_date')  
    list_filter = ('author', 'price', 'return_due_date')  
    search_fields = ('title', 'author')  

    def cover_preview(self, obj):
        """ Display a preview of the book cover in the admin panel. """
        image_url = obj.book_img_url()
        print(image_url)
        if image_url and image_url != "No Image":
            return format_html('<img src="{}" width="100" height="150" style="border-radius: 10px;"/>', image_url)
        return "No Image"
    
    cover_preview.short_description = "Book Cover"  # Custom column name

admin.site.register(Book, BookAdmin)
