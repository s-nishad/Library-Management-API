import datetime
from django.db import transaction
from django.utils.timezone import now
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from book.models import Book, BookBorrow
from book.serializers import BookSerializer, BookBorrowerSerializer, BookReturnSerializer, BorrowedBookDetailsSerializer
from user.permissions import IsMember, IsAdmin


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowBookAPIView(CreateAPIView):
    permission_classes = [IsMember]
    serializer_class = BookBorrowerSerializer

    def create(self, request, *args, **kwargs):
        books = request.data.get('books', [])
        if not books:
            return Response({'error': 'No books provided'}, status=status.HTTP_400_BAD_REQUEST)

        unavailable_books = []
        valid_books = []
        for book_id in books:
            try:
                book = Book.objects.get(pk=book_id)
                if book.status == 'available':
                    valid_books.append(book)
                else:
                    unavailable_books.append(f"Book '{book.title}' is not available, already borrowed")
            except Book.DoesNotExist:
                unavailable_books.append(f"Book ID {book_id} does not exist.")

        if unavailable_books:
            return Response({"error": unavailable_books}, status=status.HTTP_400_BAD_REQUEST)

        # Check Borrowing Limit
        active_borrows = BookBorrow.objects.filter(user=request.user, is_returned=False).count()
        if active_borrows + len(valid_books) > 5:
            return Response({"error": "Borrow limit reached. You cannot borrow more than 5 books at a time."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Perform Borrow Operation
        with transaction.atomic():
            borrow = BookBorrow.objects.create(
                user=request.user
            )
            borrow.books.set(valid_books)
            borrow.save()

            for book in valid_books:
                book.status = 'borrowed'
                book.save()

        return Response(BookBorrowerSerializer(borrow).data, status=status.HTTP_201_CREATED)


class ReturnBookAPIView(UpdateAPIView):
    permission_classes = [IsMember]
    queryset = BookBorrow.objects.all()
    serializer_class = BookReturnSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_returned:
            return Response({"error": "Books have already been returned."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark as returned
        instance.return_date = now()
        instance.fine = instance.calculate_fine()
        instance.is_returned = True

        instance.save()

        # Update book statuses
        books = instance.books.all()
        for book in books:
            book.status = 'available'
            book.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BorrowedBookDetails(ListAPIView):
    serializer_class = BorrowedBookDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'member':
            return BookBorrow.objects.filter(user=self.request.user, is_returned=False)
        if user.role == 'admin':
            return BookBorrow.objects.all()


class AvailableBooksAPIView(ListAPIView):
    queryset = Book.objects.filter(status='available')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(status='available')

