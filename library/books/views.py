
from rest_framework import viewsets

from libs.pagination import ResultSetPagination

from books.models import Book, Genre
from books.serializers import BookSerializer, GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = ResultSetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = ResultSetPagination
