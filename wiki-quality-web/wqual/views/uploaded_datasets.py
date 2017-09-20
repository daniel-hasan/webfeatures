'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a upload dos datasets
'''
from django.views.generic.list import ListView

from wqual.models import Dataset


class DatasetListView(ListView):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os datasets de um usuário. 
    '''
    #filtrar por usuario logado
    model = Dataset
    template_name = "content/dataset_list.html"
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user) if  self.request.user.is_authenticated() else []
    
    