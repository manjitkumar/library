from rest_framework import serializers

from books.models import Book, Genre


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'isbn', 'genre', 'authors')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'genre')
