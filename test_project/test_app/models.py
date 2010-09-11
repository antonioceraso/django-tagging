from django.db import models
from tagging.fields import TagField


class Book(models.Model):
    name = models.CharField(max_length=100)
    tags = TagField()
    
    def __unicode__(self):
        return self.name
