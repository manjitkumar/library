from django.db import models

from libs.models import TimeStampedModel


class Book(TimeStampedModel):
    """
    Book model keeps all the information about the books available in the
    library.
    """
    title = models.CharField(max_length=256)
    description = models.TextField(null=True)
    isbn = models.CharField(max_length=16)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    genre = models.ManyToManyField('Genre')
    authors = models.ManyToManyField('authors.Author')

    class Meta:
        db_table = 'book'

    def __unicode__(self):
        return unicode(self.title)


class Genre(TimeStampedModel):
    """
    Genre model keeps all the information about the genres about the books
    available in the library.
    """
    GENRES_LIST = (
        ('scifi', 'Science Fiction'),
        ('satire', 'Satire'),
        ('drama', 'Drama'),
        ('action and adventure', 'Action and Adventure'),
        ('romance', 'Romance'),
        ('mystery', 'Mystery'),
        ('horror', 'Horror'),
    )
    genre = models.CharField(max_length=32, choices=GENRES_LIST, unique=True)

    class Meta:
        db_table = 'genre'

    def __unicode__(self):
        return unicode(self.genre)
