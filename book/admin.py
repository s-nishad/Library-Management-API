from django.contrib import admin
from book.models import Book, BookBorrow


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(BookBorrow)
class BookBorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'borrow_date', 'return_deadline', 'is_returned', 'return_date', 'fine')
