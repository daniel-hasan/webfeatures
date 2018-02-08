'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a configuração das features
'''
from django.forms.utils import ErrorList
from django.http.response import JsonResponse, HttpResponse, \
    HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from utils.basic_entities import LanguageEnum
from wqual.models.featureset_config import FeatureSet, Language, UsedFeature, \
    UsedFeatureArgVal, FeatureFactory


class FormValidation(object):
    def form_valid(self, view, form):
        form.instance.user = view.request.user
        lst_featureSet = FeatureSet.objects.filter(user=view.request.user,
                                                   nam_feature_set=form.instance.nam_feature_set)
        if(form.instance.pk != None):
            lst_featureSet = lst_featureSet.exclude(pk=form.instance.pk)
        if len(lst_featureSet) > 0:
            errors = form._errors.setdefault("nam_feature_set", ErrorList())
            errors.append(u"nam_feature_set já existe. Ação não permitida")
            return False
        
        return True
    
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
    fields=["nam_feature_set","dsc_feature_set", "language"]
    initial = { 'language': Language.objects.get(name=LanguageEnum.en.name) }
    
    model = FeatureSet
    template_name = "content/feature_set_update_insert.html"
    form_validator = FormValidation()

    def form_valid(self, form):
        
        bol_valid = FeatureSetInsert.form_validator.form_valid(self, form)
        return super(CreateView, self).form_valid(form) if bol_valid else super(CreateView, self).form_invalid(form)
     
    def get_queryset(self):
        return FeatureSet.objects.filter(user=self.request.user) if  self.request.user.is_authenticated() else []
    
    def get_success_url(self):
        return reverse('feature_set_list')
    
    class Meta:
        labels = {
            "nam_feature_set" : "Name Feature Set",
            "dsc_feature_set" : "Description Feature Set",
            "language" : "Language"
        } 
      
class FeatureSetEdit(UpdateView):
    '''
    Created on 14 de ago de 2017
    sddasd
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''
    fields=["nam_feature_set","dsc_feature_set", "language"]
    initial = { 'language': Language.objects.get(name=LanguageEnum.en.name) }
    form_validator = FormValidation()
    model = FeatureSet

    template_name = "content/feature_set_update_insert.html"
    
    def form_valid(self, form):
        
        bol_valid = FeatureSetEdit.form_validator.form_valid(self, form)
        return super(UpdateView, self).form_valid(form) if bol_valid else super(UpdateView, self).form_invalid(form)
    
    
    def get_object(self):
        return FeatureSet.objects.get(user=self.request.user,nam_feature_set=self.kwargs["nam_feature_set"])
    
    def get_success_url(self):
        return reverse('feature_set_list')

     
class UsedFeatureListView(ListView):
    '''
    Created on 14 de ago de 2017
   
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''
   
    model = UsedFeature
    
    template_name = "content/used_features.js"
    def get_queryset(self):
        return {1:[{"used_feature_id":1,"nam_argument":"name","val_argument":"lalala","is_configurable":False},
                   {"used_feature_id":1,"nam_argument":"description","val_argument":"xuxu","is_configurable":False},
                   {"used_feature_id":1,"nam_argument":"llalala","val_argument":"eeeeee","is_configurable":True}],
                2:[{"used_feature_id":2,"nam_argument":"name","val_argument":"l3lele","is_configurable":False},
                   {"used_feature_id":2,"nam_argument":"description","val_argument":"xaxa","is_configurable":False},
                   {"used_feature_id":2,"nam_argument":"llalala","val_argument":"eeeeee","is_configurable":True}]}
        '''
        obj_Feature_Set = FeatureSet.objects.get(user=self.request.user,nam_feature_set=self.kwargs["nam_feature_set"])
        arr_used_features_set = UsedFeature.objects.filter(feature_set__pk = obj_Feature_Set.id)
        arr_used_features = UsedFeatureArgVal.objects.filter(used_feature__feature_set__id = obj_Feature_Set.id,  nam_argument__in=["name","description"])\
                                  .values("used_feature_id","nam_argument","val_argument", "is_configurable", "used_feature__feature_set__nam_feature_set", "used_feature__feature_set__dsc_feature_set")                                                
        #return arr_used_features 
       
        map_used_feat_per_id = {}
        
        for mapused in arr_used_features:
            id_feature = mapused['used_feature_id']
            
            if id_feature not in map_used_feat_per_id:
                map_used_feat_per_id[id_feature] = []
            map_used_feat_per_id[id_feature].append(mapused)

        return map_used_feat_per_id
        '''

class UsedFeatureListViewTeste(ListView):
    '''
    Created on 14 de ago de 2017
   
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''
   
    model = UsedFeature
    template_name = "content/used_feature.js"
    def get_queryset(self):
       # obj_Feature_Set = FeatureSet.objects.get(user = self.request.user,nam_feature_set = self.kwargs["nam_feature_set"])
       # arr_used_features_set = UsedFeature.objects.filter(feature_set__pk = obj_Feature_Set )
       # return arr_used_features_set 
        obj_Feature_Set = UsedFeature.objects.all().order_by('ord_feature')
        return obj_Feature_Set    

    def get_success_url(self):
        return reverse('feature_set_list')
    

class FeatureSetDelete(DeleteView):
    model = FeatureSet
    template_name = "content/feature_set_delete.html"
    
    def get_object(self):
        return FeatureSet.objects.get(user=self.request.user,nam_feature_set=self.kwargs["nam_feature_set"])
     
    def get_success_url(self):
        return reverse_lazy('feature_set_list')
    
    
    
    
class ListFeaturesView(View):
    '''
    Created on 07 de fev de 2018
   
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''    
    def get_features(self,strLanguageCode):
        """
           Obtem features e processa elas já no formato a ser retornado para o ajax
        """
        #obtem as features 
        feat_obj_list = FeatureFactory.objects.get_all_features_from_language(Language.objects.get(name=strLanguageCode))
        
        #agrupa elas por um id criado, adicionando em feature_list este id
        dict_feat_per_id = {}
        id = 1
        for objFeature in feat_obj_list:
            
            dict_feat_per_id[id] = objFeature
            id = id+1
        return dict_feat_per_id
        
    def post(self, request):
        strLanguageCode = self.kwargs["nam_language"]
        str_key_feat_per_id = "dict_feat_per_id_"+strLanguageCode
        #obtem o mapa de features por id
        dict_feat_per_id = {}
        if str_key_feat_per_id in request.session:
            #lista as features e adiciona um id para cada uma (retornando este discionario) 
            dict_feat_per_id = self.get_features(self.kwargs["nam_language"])
            request.session[str_key_feat_per_id] = dict_feat_per_id
        else:
            dict_feat_per_id =request.session[str_key_feat_per_id] 
        arr_features = []
        for idFeature,objFeature in dict_feat_per_id.items():
            arr_features.append({"id":idFeature,
                               "name":objFeature.name,
                               "description":objFeature.description,
                               "reference":objFeature.reference})
            
            
        return JsonResponse(arr_features)
    
class InsertUsedFeaturesView(View):
    def post(self, request):
        arrHidUsedFeaturesToInsert = [int(strId) for strId in self.POST["hidUsedFeaturesToInsert"].split(",")]
        UsedFeature.objects.insert_features_object(arrHidUsedFeaturesToInsert)
        return HttpResponseRedirect(reverse('feature_set_edit_features', args=[self.kwargs["nam_feature_set"]]))
