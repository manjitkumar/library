from django.db import models


class TimeStampedModel(models.Model):
    """
    TimeStampedModel is an abstract model to add following fields in every
    model where it is inherited.
      - install_ts
      - update_ts
    """
    install_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
