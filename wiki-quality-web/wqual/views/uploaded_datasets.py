'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a upload dos datasets
'''
from datetime import datetime
from django.views.generic.edit import CreateView

from wqual.models import Dataset
from wqual.models.uploaded_datasets import Status, StatusEnum


class DatasetCreateView(CreateView):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os datasets de um usuário. 
    '''
    #filtrar por usuario logado
    fields=["format", "feature_set"]
    
    model = Dataset
    template_name = "content/dataset_list.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.nam_dataset = self.request.FILES['nam_dataset']
        form.instance.status = Status.objects.get_enum(StatusEnum.PROCESSING)
        form.instance.dat_submitted = datetime.now()
        return super(CreateView, self).form_valid(form)

    #def get_queryset(self):
    #    obj = Status.objects.get_enum(StatusEnum.PROCESSING)
    #    return Dataset.objects.filter(user=self.request.user) if  self.request.user.is_authenticated() else []

    
    def get_context_data(self, **kwargs):
        context = super(DatasetCreateView, self).get_context_data(**kwargs)
        context['dataset_list'] = Dataset.objects.all()
        return context         
            
    class Meta:
        labels = {
            "format" : "Format Dataset",
            "feature_set" : "Feature Set Dataset"
        }
    