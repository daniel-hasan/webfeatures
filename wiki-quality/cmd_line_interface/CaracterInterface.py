import json
from feature.features import FeatureDocumentsReader, FeatureDocumentsWriter, FeatureCalculator, ReviewBasedFeature, GraphBasedFeature
from feature.features import Document as DocumentFeature
from feature.feature_factory.feature_factory import FeatureFactory
from utils.uncompress_data import CompressedFile
from utils.basic_entities import LanguageEnum

class DatasetDocReader(FeatureDocumentsReader):
    def __init__(self, dataset):
        self.dataset = dataset

    def get_documents(self):

        with open(self.dataset,"rb") as file:
            file_zip = CompressedFile.get_compressed_file(file)

            for name,strFileTxt in file_zip.read_each_file():
                yield DocumentFeature(name,name,str(strFileTxt))


class DatasetDocWriter(FeatureDocumentsWriter):
    def __init__(self, datasetfile):
        self.datasetfile = datasetfile
        self.data = {"header":{},"data":{}}

    def write_header(self,arr_features):
        
        carr = CaracterInterface()
        arr_features = carr.obtemObjetosFeatures(arr_features.get("arr_features"))
        arr_feat = enumerate(arr_features)
        
        for i,objFeature in arr_feat:
            self.data["header"][i]= {"name":objFeature.name, "params":objFeature.get_params_str()}
        
        return arr_features

    def write_document(self,document,arr_feats_used,arr_feats_result):
        
        self.document = document
        self.arr_feats_used = arr_feats_used
        self.arr_feats_result = arr_feats_result
        self.data["data"][self.document.int_doc_id] = self.arr_feats_result
        
    def write_graph(self,name_feature_graph,result):
        self.data["data"][name_feature_graph] = result

    def finishAllDocuments(self):

        with open(self.datasetfile,"w") as file:
            json.dump(self.data,file)



class CaracterInterface:

    def execute(self,zipfile,result_datasetfile,arr_features_to_extract,format):
        #zipfile: nome do zip com arquivos contendo texto para serem processados ou o arquivo csv com informações sobre o grafo
        #result_datasetfile: nome do arquivo de saida
        #arr_features_to_extract: gerado por meio do le_arquivo
        #format: FormatEnum.text_plain
        
        if(format == "textplain" or format == "html"):
            datReader = DatasetDocReader(zipfile) #descompacta o arquivo zip de entrada (que contém os textos)
            
        if(format == "graph"):
            datReader = zipfile
        
        docWriter = DatasetDocWriter(result_datasetfile) #arquivo saida
        saida = FeatureCalculator.featureManager.computeFeatureSetDocuments(datReader,docWriter,arr_features_to_extract,format)
        return saida
        
    def le_arquivo(self,arq_json):
        arq_json = open(arq_json,"r")
        features = json.loads(arq_json.read())
        arq_json.close()
        return features



    def obtemObjetosFeatures(self,arrNomesFeatures):
            objEnglish = LanguageEnum.en
            dictFeatures = {}
            arr_obj_features = []
            #cria um dicionário com todas as features em que as chaves são os nomes delas
            for SubClass in FeatureFactory.__subclasses__():
                objFeatFact = None
                if(SubClass.IS_LANGUAGE_DEPENDENT):
                    objFeatFact = SubClass(objEnglish)#Passar o idioma correto
                else:
                    objFeatFact = SubClass()

                for feat in objFeatFact.createFeatures():
                    dictFeatures[feat.name] = feat #para cada feature cria uma instancia no dicionario com o nome da feature
            
            #Verifica se todas as features recebidas do usuário pelo arquivo JSON existem
            for feature in arrNomesFeatures:
                opcao = 0
                if(type(feature)==str):
                    if((feature not in dictFeatures)):
                        print(">>>>> ERROR! A feature '"+feature+"' não foi encontrada.")
                        opcao = input(">>>>> Deseja continuar mesmo assim? 0-NÃO 1-SIM ")
                        if (opcao==0):
                            sys.exit()
                        else:
                            arrNomesFeatures.remove(feature)
                            
            for feature in arrNomesFeatures:
                
                type_ent = type(feature)
                obj_feature = None
                if type_ent == str:
                    obj_feature = dictFeatures[feature]
                elif type_ent == dict:
                    obj_feature = dictFeatures[feature["name"]]
                    if "param" in feature:
                        for param_name,param_value in feature["param"].items():
                            obj_feature.addConfigurableParam(param_name)
                            obj_feature.__dict__[param_name] = param_value

                arr_obj_features.append(obj_feature)
            return arr_obj_features


    def imprimirFeatures(self):
        arr_feat_name = []
        arr_feature_factories = []
        objEnglish = LanguageEnum.en
        for SubClass in FeatureFactory.__subclasses__(): #percorre todas as features
            objFeatFact = None
            if(SubClass.IS_LANGUAGE_DEPENDENT):
                objFeatFact = SubClass(objEnglish)# instancia as features de acordo com o idioma
            else:
                objFeatFact = SubClass()
            arr_feature_factories.append(objFeatFact)

        for objFeatFact in arr_feature_factories:
            for feat in objFeatFact.createFeatures():
                arr_feat_name.append(feat.name) #adiciona o nome das features no vetor arr
                
        arr_feat_name.sort()
        for name in arr_feat_name:
            print(name)    #printa o nome de todas as features
        return arr_feat_name
    
    def gera_arqtest(self):
        
        arr_feat_name = []
        arr_feature_factories = []
        objEnglish = LanguageEnum.en
        dictFeatures = {}
        arr_obj_features = []
        
        for SubClass in FeatureFactory.__subclasses__(): #percorre todas as features
            objFeatFact = None
            if(SubClass.IS_LANGUAGE_DEPENDENT):
                objFeatFact = SubClass(objEnglish)# instancia as features de acordo com o idioma
            else:
                objFeatFact = SubClass()
                    
            arr_feature_factories.append(objFeatFact)

        for objFeatFact in arr_feature_factories:
            for feat in objFeatFact.createFeatures():
                if(isinstance(feat, GraphBasedFeature)==False and isinstance(feat, ReviewBasedFeature)==False):
                    if(feat.arr_configurable_param!=[]):
                        dic_param = {}
                        for param in feat.arr_configurable_param:
                            dic_param[param.name] = param.default_value
                        feat_com_parametro = {"name":feat.name,"param":dic_param}
                        arr_feat_name.append(feat_com_parametro)
                    else:
                        arr_feat_name.append(feat.name)
        
        lista_features = arr_feat_name
        conteudo_arquivo_json = {}
        conteudo_arquivo_json["arr_features"] = lista_features
        conteudo_arquivo_json = json.dumps(conteudo_arquivo_json)
        arquivo_json = open("cmd_line_interface/arqtest.json","w")
        arquivo_json.write(conteudo_arquivo_json)
        arquivo_json.close()
        return arr_feat_name
    
    def gera_arqtest_graph(self):
        
        arr_feat_name = []
        arr_feature_factories = []
        objEnglish = LanguageEnum.en
        dictFeatures = {}
        arr_obj_features = []
        
        for SubClass in FeatureFactory.__subclasses__(): #percorre todas as features
            objFeatFact = None
            if(SubClass.IS_LANGUAGE_DEPENDENT):
                objFeatFact = SubClass(objEnglish)# instancia as features de acordo com o idioma
            else:
                objFeatFact = SubClass()
                    
            arr_feature_factories.append(objFeatFact)

        for objFeatFact in arr_feature_factories:
            for feat in objFeatFact.createFeatures():
                if(isinstance(feat, GraphBasedFeature)):
                    if(feat.arr_configurable_param!=[]):
                        dic_param = {}
                        for param in feat.arr_configurable_param:
                            dic_param[param.name] = param.default_value
                        feat_com_parametro = {"name":feat.name,"param":dic_param}
                        arr_feat_name.append(feat_com_parametro)
                    else:
                        arr_feat_name.append(feat.name)
        
        lista_features = arr_feat_name
        conteudo_arquivo_json = {}
        conteudo_arquivo_json["arr_features"] = lista_features
        conteudo_arquivo_json = json.dumps(conteudo_arquivo_json)
        arquivo_json = open("cmd_line_interface/graph_arqtest.json","w")
        arquivo_json.write(conteudo_arquivo_json)
        arquivo_json.close()
        return arr_feat_name
        
    

if __name__ == "__main__":
    
    import sys
    car = CaracterInterface()

    if(sys.argv[1] == "-L"):
        print("Lista de features:")
        print(car.imprimirFeatures())
    else:
        nome_arquivo_zip = sys.argv[1]
        nome_arquivo_json = sys.argv[2]
        nome_arquivo_saida = sys.argv[3]
        format = sys.argv[4]
        arr_features_to_extract = car.le_arquivo(nome_arquivo_json)
        saida = car.execute(nome_arquivo_zip, nome_arquivo_saida, arr_features_to_extract, format)
