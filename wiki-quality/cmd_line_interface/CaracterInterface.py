import json
from feature.features import FeatureDocumentsReader, FeatureDocumentsWriter, FeatureCalculator
from feature.features import Document as DocumentFeature
from utils.uncompress_data import CompressedFile

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
        datReader = DatasetDocReader(zipfile)
        docWriter = DatasetDocWriter(result_datasetfile)
        FeatureCalculator.featureManager.computeFeatureSetDocuments(datReader,docWriter,arr_features_to_extract,format)

    def le_arquivo(arq_json):
        """
        class X():
            def __init__(self):
                self.y = 1
                self.a = 2

        dicionario = {"y":3,
                    "a":4}
        feat = X()
        for att,val in dicionario.items():

            feat.__dict__[att]  = val

        """
        #ler do JSON e retorna vetor de strings
        features = json.loads(open(arq_json).read())

        #obtem arr_Nomes_features type()
        {"arr_features":["Readability","Feautre bonitinha","feature linda",
                          {"name":"featurelinda",
                        "param":{"word_count_max":10}}]}

        return features#



    def obtemObjetosFeatures(self,arrNomesFeatures):
        dictFeatures = {}
        arr_obj_featurres = []
        #cria um dicionário com todas as features em que as chaves são os nomes delas
        for SubClass in FeatureFactory.__subclasses__():
            objFeatFact = None
            if(SubClass.IS_LANGUAGE_DEPENDENT):
                objFeatFact = SubClass(objEnglish)#Passar o idioma correto
            else:
                objFeatFact = SubClass()

            for feat in objFeatFact.createFeatures():
                dictFeatures[feat.name] = feat          #para cada feature cria uma instancia no dicionario com o nome da feature
        for feature in arrNomesFeatures:
            arr_obj_features.append(dictFeature[feature])
        return arr_obj_features
        
    def imprimirFeatures(self):
        for SubClass in FeatureFactory.__subclasses__(): #percorre todas as features
            objFeatFact = None
            if(SubClass.IS_LANGUAGE_DEPENDENT):
                objFeatFact = SubClass(objEnglish)# instancia as features de acordo com o idioma
            else:
                objFeatFact = SubClass()
        for feat in objFeatFact.createFeatures():
            print(feat.name)    #printa o nome de todas as features
        return arr

	###################################################################
	#IF mmain
if __name__ == "__main__":
	import sys
	if(sys.argv[1] == "-L"):
		print("Lista de features:")	#printa a lista de features
		print(imprimirFeatures())
	else:
		arrNomesFeatures = func(sys.argv[1])
		#Dict=obtemObjetosFeatures(arrNomesFeatures)
