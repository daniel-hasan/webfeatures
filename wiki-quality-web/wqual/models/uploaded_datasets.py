'''
Created on 14 de ago de 2017

@author: profhasan
'''
from django.contrib.auth.models import User
from django.db import models

from utils.basic_entities import Format
from wqual.models import FeatureSet


class Status(models.Model):
    name = models.CharField(max_length=45)
    
class Dataset(models.Model):
    name = models.CharField(max_length=45)
    submitted_date = models.CharField(max_length=45)
    valid_until = models.DateTimeField(blank=True, null=True)
    format = models.CharField(max_length=10,choices = [(f.name,f) for f in Format])    
    
    feature_set = models.ForeignKey(FeatureSet, models.PROTECT)
    user = models.ForeignKey(User, models.PROTECT)
    status = models.ForeignKey(Status, models.PROTECT)

    @property
    def format_enum(self):
        return Format[self.format]
    
class Document(models.Model):
    text = models.TextField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    
    dataset = models.ForeignKey(Dataset, models.PROTECT)