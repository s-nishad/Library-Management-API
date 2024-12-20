from django.urls import path, include

from rest_framework.routers import DefaultRouter
from book.views import BookViewSet, BorrowBookAPIView, ReturnBookAPIView, BorrowedBookDetails, AvailableBooksAPIView

app_name = 'book'

router = DefaultRouter()
router.register('library', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),

    path('borrow/', BorrowBookAPIView.as_view(), name='borrow_books'),
    path('borrow/<int:id>/return/', ReturnBookAPIView.as_view(), name='return_books'),
    path('available-books/', AvailableBooksAPIView.as_view(), name='available_books'),
    path('borrowed-list/', BorrowedBookDetails.as_view(), name='borrowed-list'),

]
