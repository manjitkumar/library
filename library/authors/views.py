
from rest_framework import viewsets

from libs.pagination import ResultSetPagination

from authors.models import Author
from authors.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = ResultSetPagination
