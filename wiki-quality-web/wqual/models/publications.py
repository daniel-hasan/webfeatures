'''
Created on 14 de ago de 2017

@author: profhasan
'''
from django.db import models

    
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class Conference(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)


class Publication(models.Model):
    title = models.CharField(max_length=400)
    year = models.IntegerField()
    
    authors = models.ManyToManyField(Author)
    conference = models.ForeignKey(Conference, models.PROTECT)
    