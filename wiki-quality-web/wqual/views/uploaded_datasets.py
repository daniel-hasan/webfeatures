'''
Created on 14 de ago de 2017

@author: profhasan
'''
from django.views.generic.list import ListView

from wqual.models import Dataset


class DatasetListView(ListView):
    #filtrar por usuario logado
    model = Dataset
    template_name = "content/dataset_list.html"
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)