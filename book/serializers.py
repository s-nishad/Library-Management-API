from django.utils import timezone

from rest_framework import serializers
from book.models import Book, BookBorrow


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookBorrowerSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), many=True)

    class Meta:
        model = BookBorrow
        fields = '__all__'
        read_only_fields = ['return_date', 'return_deadline', 'is_returned', 'fine', 'user']


class BookReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookBorrow
        fields = ['id', 'user', 'books', 'return_date', 'is_returned', 'fine']
        read_only_fields = ['fine', 'return_date', 'books', 'is_returned']

    def validate(self, attrs):
        if self.instance.is_returned:
            raise serializers.ValidationError("This book borrow instance has already been marked as returned.")
        return attrs


class BorrowedBookDetailsSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True)

    class Meta:
        model = BookBorrow
        fields = ['id', 'books', 'borrow_date', 'return_deadline', 'is_returned', 'user']
