'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a configuração das features
'''
from django.views.generic.list import ListView

from wqual.models import FeatureSet


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