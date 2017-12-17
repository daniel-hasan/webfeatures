'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a upload dos datasets
'''
from datetime import datetime
from django import forms
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FileField
from django.urls.base import reverse
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
import lzma
from utils.uncompress_data import *
from wqual.models import Dataset
from wqual.models.uploaded_datasets import Format, Status, StatusEnum, DocumentText, \
    Document


class DatasetCreateView(CreateView, ListView):
    '''
    Created on 14 de ago de 2017
    
    @author: Raphael Luiz
    Cria um dataset de um usuário. 
    '''
    
    fields=["format", "feature_set"]
    
    model = Dataset
    template_name = "content/dataset_list.html"
    
 
    def descompacta(self):
        return lzma.decompress(self.arquivo).decode("utf-8")
    
    def upload_file(self, request, form):
        if request.method == 'POST':
            dataset_file = Document.objects.create(nam_file=self.name,dataset=form.instance)
        if dataset_file.is_valid():
            dataset_file.save()
            
    def get_context_data(self, **kwargs):
        context = super(DatasetCreateView, self).get_context_data(**kwargs)
        context['dataset_list'] = Dataset.objects.filter(user=self.request.user) if self.request.user.is_authenticated() else []
        return context    
        
    def form_valid(self, form):
        if form.feature_set.Format == 'HTML':
            if form.Format.value == 'text_plain':
                messages.warning(form, "If you wish to send, it won't be possible to extract the features that extract information from the HTML.")
        form.instance.user = self.request.user
        form.instance.nam_dataset = self.request.FILES['file_dataset'].name
        form.instance.status = Status.objects.get_enum(StatusEnum.PROCESSING)
        form.instance.dat_submitted = datetime.now()
        
        #save (tratar a exceção: e adicionar erro na lista de erro e retonrar form_invalid se houver exceção)
        form.instance.save_compressed_file(self.request.FILES['file_dataset'])
        
        return super(CreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('extract_features')  
            
    class Meta:
        labels = {
            "format" : "Format Dataset",
            "feature_set" : "Feature Set Dataset"
        }
        
             
class DatasetDelete(DeleteView):
        '''
        Created on 7 dez de 2017
        
        @author: Raphael Luiz
        Exclui um dataset.
        '''
        
        model = Dataset
        template_name = "content/dataset_list.html"#colocar o nome de um template aqui.
        
        def get_object(self):
            return Dataset.objects.get(user=self.request.user,nam_dataset=self.kwargs["nam_dataset"])
        
        def get_success_url(self):
            return reverse('extract_features')
            