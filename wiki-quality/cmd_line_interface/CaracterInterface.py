import json
from feature.features import FeatureDocumentsReader, FeatureDocumentsWriter, FeatureCalculator
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
        arr_feat = enumerate(arr_features)
        for i,objFeature in arr_feat:
            self.data["header"][i]= {"name":objFeature.name, "params":objFeature.get_params_str()}

    def write_document(self,document, arr_feats_used, arr_feats_result):
        self.document = document
        self.arr_feats_used = arr_feats_used
        self.arr_feats_result = arr_feats_result

        self.data["data"][self.document.int_doc_id] = self.arr_feats_result

    def finishAllDocuments(self):

        with open(self.datasetfile,"w") as file:
            json.dump(self.data,file)



class CaracterInterface:

    def execute(self,zipfile,result_datasetfile,arr_features_to_extract,format):
        """
        zipfile: nome do zip com arquivos contendo texto para serem processados
        result_datasetfile: nome do arquivo de saida
        arr_features_to_extract: gerado por meio do le_arquivo
        format: FormatEnum.text_plain
        """
        datReader = DatasetDocReader(zipfile)
        docWriter = DatasetDocWriter(result_datasetfile)
        FeatureCalculator.featureManager.computeFeatureSetDocuments(datReader,docWriter,arr_features_to_extract,format)

    def le_arquivo(self,arq_json):
        features = json.loads(open(arq_json).read())
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

            for feature in arrNomesFeatures:
                type_ent = type(feature)

                obj_feature = None

                if type_ent == str:
                    obj_feature = dictFeatures[feature]
                elif type_ent == dict:
                    obj_feature = dictFeatures[feature["name"]]
                    if "param" in feature:
                        for param_name,param_value in feature["param"].items():
                            obj_feature.__dict__[param_name] = param_value

                arr_obj_features.append(obj_feature)
            return arr_obj_features


    def imprimirFeatures(self):
        arr = []
        objEnglish = LanguageEnum.en
        for SubClass in FeatureFactory.__subclasses__(): #percorre todas as features
            objFeatFact = None
            if(SubClass.IS_LANGUAGE_DEPENDENT):
                objFeatFact = SubClass(objEnglish)# instancia as features de acordo com o idioma
            else:
                objFeatFact = SubClass()
        for feat in objFeatFact.createFeatures():
            arr.append(feat.name)
            print(feat.name)    #printa o nome de todas as features
        return arr

if __name__ == "__main__":
    import sys
    if(sys.argv[1] == "-L"):
        print("Lista de features:")	#printa a lista de features
        car = CaracterInterface()
        print(car.imprimirFeatures())
    else:
        #<arquivozip> <json com as features> <arquivo de saida>

        #executar o le arquivo
        arrNomesFeatures = func(sys.argv[1])
        #Dict=obtemObjetosFeatures(arrNomesFeatures)
