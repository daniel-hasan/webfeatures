'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a upload dos datasets
'''
from _io import BytesIO
from datetime import datetime

import json
import lzma
import os
import uuid



from django.forms.utils import ErrorList
from django.http import HttpResponse
import zipfile
from django.urls.base import reverse
from django.views.generic.base import View
from django.views.generic.edit import CreateView, DeleteView
from wqual.models import Dataset
from wqual.models.exceptions import FileSizeException
from wqual.models.uploaded_datasets import  Status, StatusEnum, DocumentText, \
    Document, DocumentResult



class DatasetDownloadView(View):
    def get(self, request, dataset_id,format):
        
        txt_file_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/tmp/"+str(uuid.uuid1())
        #print(txt_file_name)
        
        s = BytesIO()
        zf = zipfile.ZipFile(s, "w")
        with open(txt_file_name+"."+format, "w") as f:
            if(format=="json"):
                f.write("{\n")
                f.write("\t\"feature_descriptions\":"+Dataset.objects.get(id=dataset_id).dsc_result_header+",\n")
                f.write("\t\"data\": [")
                for document in Document.objects.all().filter(dataset_id=dataset_id):
                    strResult = "{\"docname\":" + document.nam_file
                    for doc_result in DocumentResult.objects.filter(document = document):
                        arrFeatures = ["\""+str(i)+"\":"+str(feat) for i,feat in enumerate(json.loads(doc_result.dsc_result)) ]
                        strResult = strResult + ", \"result\": {" +(",".join(arrFeatures))+"}"
                    strResult = strResult + "},\n"
                    f.write(strResult)
                f.write("\t]\n")
                f.write("}")
            else:
                dictArrFeatures = json.loads(Dataset.objects.get(id=dataset_id).dsc_result_header)
                #print header
                f.write("doc_name")
                i=0
                #print("FEATUS: "+str(dictArrFeatures))
                while(str(i) in dictArrFeatures):
                    f.write(","+dictArrFeatures[str(i)]['name'])
                    i = i+1
                f.write("\n")
                
                #print each line per doc
                for document in Document.objects.all().filter(dataset_id=dataset_id):
                    strResult = document.nam_file+","
                    for doc_result in DocumentResult.objects.filter(document = document):
                        arrFeatures = [str(feat) for i,feat in enumerate(json.loads(doc_result.dsc_result)) ]
                        strResult = strResult +(",".join(arrFeatures))
                    strResult = strResult + "\n"
                    f.write(strResult)    
                    
                                    
        zf.write(txt_file_name+"."+format,arcname="result."+format, compress_type=zipfile.ZIP_DEFLATED)   
        zf.close()
        os.remove(txt_file_name+"."+format)

                
        resp = HttpResponse(s.getvalue(), content_type="application/force-download")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % "result.zip"



        
        return resp
class DatasetCreateView(CreateView):
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
        #context['map_feathtml'] = UsedFeature.objects.get_html_features_name_grouped_by_featureset()
        context['dataset_list'] = Dataset.objects.filter(user=self.request.user) if self.request.user.is_authenticated else []
        return context    
        
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.nam_dataset = self.request.FILES['file_dataset'].name
        form.instance.status = Status.objects.get_enum(StatusEnum.SUBMITTED)
        form.instance.dat_submitted = datetime.now()
        
        #save (tratar a exceção: e adicionar erro na lista de erro e retornar form_invalid se houver exceção)
        try:
            form.instance.save_compressed_file(self.request.FILES['file_dataset'])

        except FileSizeException as e:
            errors = form._errors.setdefault("feature_set", ErrorList())
            errors.append(u"Ação não permitida. O tamanho do arquivo ultrapassa o limite de 20MB.")           
            return super(CreateView, self).form_invalid(form)
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
        template_name = "content/dataset_list.html"
        
        def get_object(self):
            return Dataset.objects.get(user=self.request.user,id=self.kwargs["id_dataset"])
        
        def get_success_url(self):
            return reverse('extract_features')