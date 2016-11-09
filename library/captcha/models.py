from django.db import models

from libs.models import TimeStampedModel


class Captcha(TimeStampedModel):
    """
    Captcha model keeps all the information about the captcha to be shown
    to user when they hit a rate limit.

    question - stores the string which is to be shown as question.
      - example: What is 2 * 4?
    answer - store the answer of the question string
      - example: 8
    image_path - (optional) stores the path of an image which contains a text
    			 from the question field.
    """
    question = models.CharField(max_length=256)
    answer = models.IntegerField()
    image_path = models.TextField(null=True)

    class Meta:
        db_table = 'captcha'

    def __unicode__(self):
        return unicode(self.question)