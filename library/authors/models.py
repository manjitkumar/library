from django.db import models

from libs.models import TimeStampedModel


class Author(TimeStampedModel):
    """
    Author model keeps all the information about the authors of the books
    available in the library.
    """
    first_name = model.CharField(max_length=32)
    last_name = model.CharField(null=32)

    class Meta:
        db_table = 'author'

    def __unicode__(self):
        return unicode(self.first_name)
