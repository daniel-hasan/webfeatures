from django.contrib import admin

from wqual.models import Author, Conference, Publication
from wqual.models import Dataset
from wqual.models.featureset_config import FeatureSet, FeatureFactory, \
    UsedFeatureArgVal
from wqual.models.featureset_config import UsedFeature, Feature, Source
from wqual.models.uploaded_datasets import Status


# Register your models here.
##################### CRUD Publicações ########################
admin.site.register(Author)
admin.site.register(Conference)
admin.site.register(Publication)


#################### Dataset (para testes) ####################
admin.site.register(Dataset)
admin.site.register(FeatureSet)

####################  ####################
admin.site.register(UsedFeature)
admin.site.register(Feature)
admin.site.register(Source)
admin.site.register(FeatureFactory)

admin.site.register(UsedFeatureArgVal)
