from libs.serializers import DynamicFieldsModelSerializer
from books.models import Book, Genre


class BookSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'isbn', 'genre', 'authors')


class GenreSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'genre')
