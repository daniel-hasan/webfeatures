from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from utils.basic_entities import Language


class Feature(models.Model):
    feature_class = models.CharField(max_length=255)



class FeatureClassArgs(models.Model):
    name = models.CharField(max_length=45)
    value = models.CharField(max_length=4000)

    class Meta:
        db_table = 'wqual_feature_class_args'


class FeatureFactory(models.Model):
    class_field = models.CharField(db_column='class', max_length=45)  # Field renamed because it was a Python reserved word.

    class Meta:
        db_table = 'wqual_feature_factory'

class FeatureSetManager(models.Manager):
    def create_test_instances(self):
        #escolhe portugues e o primeiro super-usuario como dono do featureset e os cria
        obj_language = Language.pt
        obj_user = User.objects.filter(is_superuser=True).order_by('id')[0]
        self.bulk_create(
        [FeatureSet(name="Features to Assess Quality of Wikipedia",\
                    description="Those features were used to create dataset for the paper BLAH",
                    language=obj_language.name,user=obj_user),
         FeatureSet(name="Features to Assess Quality of Stack Overflow",\
                    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed at auctor nunc. Donec congue, purus a sagittis posuere, lorem lacus gravida odio, ac mattis justo est vitae est. Aenean dui ligula, suscipit non vulputate at, dignissim sed velit.",
                    language=obj_language.name,user=obj_user),
         ]
        )
    def remove_test_instances(self):
        obj_user = User.objects.filter(is_superuser=True).order_by('id')[0]
        #remove as duas featSet criadas
        self.filter(name="Features to Assess Quality of Wikipedia",user=obj_user).delete()
        self.filter(name="Features to Assess Quality of Stack Overflow",user=obj_user).delete()
        
class FeatureSet(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    
    language = models.CharField(max_length=4,choices = [(l.name,l) for l in Language])  
    user = models.ForeignKey(User, models.PROTECT)
    
    
    objects = FeatureSetManager()
    
    @property
    def language_enum(self):
        return Language[self.language]
    
    class Meta:
        db_table = 'wqual_feature_set'

    




class UsedFeature(models.Model):
    feature_set = models.ForeignKey(FeatureSet, models.PROTECT)
    feature = models.ForeignKey(Feature, models.PROTECT)
    feature_class_args = models.ForeignKey(FeatureClassArgs, models.PROTECT)

    class Meta:
        db_table = 'wqual_used_feature'
