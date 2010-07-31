from django.contrib import admin
from test_app.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'tags']
    list_editable = ['tags']
admin.site.register(Book, BookAdmin)
