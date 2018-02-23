'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a configuração das features
'''
from django.forms.utils import ErrorList
from django.views.generic.list import ListView
import json

from django.http.response import JsonResponse, HttpResponse, \
    HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from utils.basic_entities import LanguageEnum
from wqual.models.featureset_config import FeatureSet, Language, UsedFeature, \
    UsedFeatureArgVal, FeatureFactory
from django.shortcuts import render


class FormValidation(object):
    def form_valid(self, view, form):
        form.instance.user = view.request.user
        lst_featureSet = FeatureSet.objects.filter(user=view.request.user,
                                                   nam_feature_set=form.instance.nam_feature_set)
        if(form.instance.pk != None):
            lst_featureSet = lst_featureSet.exclude(pk=form.instance.pk)
        if len(lst_featureSet) > 0:
            errors = form._errors.setdefault("nam_feature_set", ErrorList())
            errors.append(u"nam_feature_set already exists.")
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

class FeatureSetInsertAJAX(View):
    
    def post(self, request):
        arrCreateFeatureSet =  json.loads(request.POST["arrCreateElementsFeatureSet"])[0]            
        FeatureSet.objects.create(user=self.request.user,nam_feature_set = arrCreateFeatureSet["nam_feature_set"], dsc_feature_set = arrCreateFeatureSet["dsc_feature_set"], language = Language.objects.get(id=int(arrCreateFeatureSet["language"])))
      
        return JsonResponse({"arrCreateFeatureSet" : arrCreateFeatureSet })
      
class FeatureSetEdit(UpdateView):
    '''
    Created on 14 de ago de 2017
    sddasd
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''
    fields=["nam_feature_set","dsc_feature_set", "language"]
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
    

class FeatureSetEditAJAX(View):
    def post(self, request):
        arrFeatureSetEdit =  json.loads(request.POST["arrEditElementsFeatureSet"])
        
        for featureSet in arrFeatureSetEdit :
            objFeatureSetEdit = FeatureSet.objects.get(user=self.request.user, nam_feature_set=featureSet["id_nam_feature_set"])
            objFeatureSetEdit.nam_feature_set = featureSet["nam_feature_set"]
            objFeatureSetEdit.dsc_feature_set = featureSet["dsc_feature_set"]
            objFeatureSetEdit.language = Language.objects.get(id=featureSet["language"])
            objFeatureSetEdit.save()
            
        return JsonResponse({"arrFeauteSetEdit" : arrFeatureSetEdit }) 

class UsedFeatureListView(ListView):
   
    model = UsedFeature
    template_name = "content/used_features.js"
    
    def get_queryset(self):
        obj_Feature_Set = FeatureSet.objects.get(user=self.request.user,nam_feature_set=self.kwargs["nam_feature_set"])
        arr_used_features = UsedFeatureArgVal.objects.filter(used_feature__feature_set__id = obj_Feature_Set.id)\
                                 .values("used_feature_id", "dsc_argument", "id", "type_argument", "nam_argument","val_argument", "is_configurable")                                                
        
        
        map_used_feat_per_id = {}
        
        for mapused in arr_used_features:
            id_feature = mapused['used_feature_id']
            
            if id_feature not in map_used_feat_per_id:
                map_used_feat_per_id[id_feature] = []
            map_used_feat_per_id[id_feature].append(mapused)

        return map_used_feat_per_id

class UsedFeatureListViewTeste(ListView):
    '''
    Created on 14 de ago de 2017
   
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todos os conjunto de features criados.
    '''        
 
   
    model = UsedFeature
    template_name = "content/used_feature.js"
    def get_queryset(self):
        obj_Feature_Set = UsedFeatureArgVal.objects.all()
        return obj_Feature_Set    

    def get_success_url(self):
        return reverse('feature_set_list')

class UsedFeatureIsConfigurableForm(View): 
    
    model = UsedFeatureArgVal
    template_name = "content/used_features.js"
    
    def post(self, request):
        arrValueArgVal =  json.loads(request.POST["id_ArgVal"])
        
        for argVal in arrValueArgVal:
            objUsedFeatureArgVal = UsedFeatureArgVal.objects.get(used_feature__feature_set__user=self.request.user, id=argVal["idArgVal"])
            objUsedFeatureArgVal.val_argument = argVal["valueArgVal"]
            objUsedFeatureArgVal.save()
            
        return JsonResponse({"arrValueArgVal" : arrValueArgVal})
        
class UsedFeatureDelete(View):
    model = UsedFeatureArgVal
    template_name = "content/used_features.js"
    
    def post(self, request):        
        UsedFeatureArgVal.objects.filter(used_feature__feature_set__user=self.request.user,used_feature_id=request.POST['used_feature_id']).delete()
        UsedFeature.objects.get(feature_set__user=self.request.user,id=request.POST['used_feature_id']).delete()
        
        return JsonResponse({})

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
    @classmethod   
    def get_features(self,strLanguageCode):
        """
           Obtem features e processa elas já no formato a ser retornado para o ajax
        """
        #obtem as features 
        feat_obj_list = FeatureFactory.objects.get_all_features_from_language(Language.objects.get(name=strLanguageCode))
        
        #agrupa elas por um id criado, adicionando em feature_list este id
        dict_feat_per_id = {}
        #idFeature = 1
        for objFeature in feat_obj_list:
            dict_feat_per_id[objFeature.name] = objFeature
            #idFeature = idFeature+1
        return dict_feat_per_id
        
    def post(self, request,nam_language):
        dict_feat_per_id = self.get_features(nam_language)
        arr_features = []
        for namFeature,objFeature in dict_feat_per_id.items():
            arr_features.append({"name":namFeature,
                               "description":objFeature.description,
                               "reference":objFeature.reference})
            
            
        return JsonResponse({"arrFeatures":arr_features})
    


class JSListAddUsedFeatureView(TemplateView):
    template_name = "content/list_add_used_features.js"    
    
class InsertUsedFeaturesView(View):
    def post(self, request,nam_feature_set):
        #get the feature set object
        objFeatureSet=FeatureSet.objects.get(user=self.request.user,nam_feature_set=nam_feature_set)
        
        #get the features to add
        arrStrFeatureNames = [strName for strName in json.loads(request.POST["hidUsedFeaturesToInsert"])]
        print(str(arrStrFeatureNames))
        
        #get all the possible features
        dict_feat_per_id = ListFeaturesView.get_features(objFeatureSet.language.name)
        
        #obtain the objects to insert by name
        arrObjFeaturesToInsert = [dict_feat_per_id[nam_feature] for nam_feature in arrStrFeatureNames]
        
        
        #inser them
        dictInsertedFeat = UsedFeature.objects.insert_features_object(objFeatureSet,arrObjFeaturesToInsert)
        
        #return the object
        arrInsertedFeatures = []
        for objFeature in arrObjFeaturesToInsert:
            objUsedFeature = dictInsertedFeat[objFeature.name]
            arrConfigParamsFeat = []
            isConfigurable = False
            for argValParam in objUsedFeature.usedfeatureargval_set.values("id","nam_argument","val_argument","type_argument","is_configurable"):
                if(argValParam['is_configurable']):
                    arrConfigParamsFeat.append(argValParam)
                    isConfigurable = True
                    
            arrInsertedFeatures.append({"used_feature_id":objUsedFeature.id,
                                        "name":objFeature.name,
                                        "description":objFeature.description+"\n"+objFeature.reference,
                                        "is_configurable":isConfigurable,
                                        "ord_feature":objUsedFeature.ord_feature,
                                        "arr_param":arrConfigParamsFeat
                                        })
            
            
        #return HttpResponseRedirect(reverse('feature_set_edit_features', args=[nam_feature_set]))
        return JsonResponse({"arrUsedFeatures":arrInsertedFeatures})
