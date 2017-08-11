# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=45)
    feature_set = models.ForeignKey('FeatureSet', models.PROTECT)
    submitted_date = models.CharField(max_length=45)
    status = models.ForeignKey('Status', models.PROTECT)
    valid_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'dataset'


class Document(models.Model):
    dataset = models.ForeignKey(Dataset, models.PROTECT)
    text = models.TextField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'document'


class Feature(models.Model):
    feature_class = models.CharField(max_length=255)

    class Meta:
        db_table = 'feature'


class FeatureClassArgs(models.Model):
    name = models.CharField(max_length=45)
    value = models.CharField(max_length=4000)

    class Meta:
        db_table = 'feature_class_args'


class FeatureFactory(models.Model):
    id = models.IntegerField(primary_key=True)
    class_field = models.CharField(db_column='class', max_length=45)  # Field renamed because it was a Python reserved word.

    class Meta:
        db_table = 'feature_factory'


class FeatureSet(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=45, blank=True, null=True)
    language = models.ForeignKey('Language', models.DO_NOTHING)

    class Meta:
        db_table = 'feature_set'


class Language(models.Model):
    name = models.CharField(max_length=45)
    language_code = models.CharField(max_length=5)

    class Meta:
        db_table = 'language'


class Status(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'status'


class UsedFeature(models.Model):
    feature_set = models.ForeignKey(FeatureSet, models.DO_NOTHING)
    feature = models.ForeignKey(Feature, models.DO_NOTHING)
    feature_class_args = models.ForeignKey(FeatureClassArgs, models.DO_NOTHING)

    class Meta:
        db_table = 'used_feature'
