'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a configuração das features
'''
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView

from wqual.models import FeatureSet,UsedFeature


# Create your views here.
class FeatureSetListView(ListView):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''
    
    model = FeatureSet
    template_name = "content/feature_set_list.html"
    def get_queryset(self):
        return FeatureSet.objects.filter(user=self.request.user) if  self.request.user.is_authenticated() else []

class FeatureSetInsert(CreateView):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''
    fields=["group","nam_feature_set","dsc_feature_set"]
    model = FeatureSet
    template_name = "content/feature_set_update_insert.html"

class FeatureSetEdit(UpdateView):
    '''
    Created on 14 de ago de 2017
    sddasd
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''
    fields=["group","nam_feature_set","dsc_feature_set"]
    model = FeatureSet

    template_name = "content/feature_set_update_insert.html"

    def get_object(self):
        return FeatureSet.objects.get(user=self.request.user,nam_feature_set=self.kwargs["nam_feature_set"])
     
class UsedFeatureListView(ListView):
    '''
    Created on 14 de ago de 2017
   
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''
   
    model = UsedFeature
    template_name = "content/used_features.js"
    def get_queryset(self):
        return UsedFeature.objects.filter(feature_set__pk=9)

class UsedFeatureListViewTeste(ListView):
    '''
    Created on 14 de ago de 2017
   
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''
   
    model = UsedFeature
    template_name = "content/used_features.html"
    def get_queryset(self):
        return UsedFeature.objects.filter(feature_set__pk=9)    