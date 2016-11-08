from django.db import models

from libs.models import TimeStampedModel


class Book(TimeStampedModel):
    """
    Book model keeps all the information about the books available in the
    library.
    """
    title = model.CharField(max_length=256)
    description = model.TextField(null=True)
    isbn = model.CharField(max_length=16)
    price = model.DecimalField(max_digits=8, decimal_places=2)
    genre = model.ManyToManyField('Genre')
    authors = model.ManyToManyField('author.Author')

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
        ('SciFi', 'Science fiction'),
        ('Satire', 'Satire'),
        ('Drama', 'Drama'),
        ('Axn & Advn', 'Action and Adventure'),
        ('Romance', 'Romance'),
        ('Mystery', 'Mystery'),
        ('Horror', 'Horror'),
    )
    genre = models.CharField(max_length=32, choices=GENRES_LIST)

    class Meta:
        db_table = 'genre'

    def __unicode__(self):
        return unicode(self.genre)
