from django.db import models

from libs.models import TimeStampedModel


class Publisher(TimeStampedModel):
    """
    Publisher model keeps all the information about the publisher of the
    books available in the library.
    """
    name = model.CharField(max_length=64)
    website = model.CharField(max_length=128)
    
    class Meta:
        db_table = 'publisher'

    def __unicode__(self):
        return unicode(self.title)
