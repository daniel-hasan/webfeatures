import json
from feature.features import Document as DocumentFeature
from utils.uncompress_data import CompressedFile

class DatasetDocReader(FeatureDocumentsReader):

    def __init__(self, dataset):
        self.dataset = dataset

    def get_documents(self):

        with open(self.dataset,"r") as file:
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
                self.data["header"][i]= {"name":objFeature.name,
                                    "params":objFeature.get_params_str()}

        def write_document(self,document, arr_feats_used, arr_feats_result):
            self.document = document
            self.arr_feats_used = arr_feats_used
            self.arr_feats_result = arr_feats_result

            data["data"][self.document.int_doc_id] = self.arr_feats_result

        def finishAllDocuments(self):

            with open(datasetfile,"w") as file:
                json.dump(self.data,file)


class CaracterInterface:


	def func(arq_json):
	    #ler do JSON e retorna vetor de strings
		features = json.loads(open(arq_json).read())


		print(features)

		return features
	##################################################################
	def obtemObjetosFeatures(arrNomesFeatures):
		dictFeatures = {}
		arr_obj_featurres = []

		for SubClass in FeatureFactory.__subclasses__():
			objFeatFact = None
			if(SubClass.IS_LANGUAGE_DEPENDENT):
				objFeatFact = SubClass(objEnglish)#Passar o idioma correo
			else:
				objFeatFact = SubClass()

			for feat in objFeatFact.createFeatures():
				dictFeatures[feat.name] = feat
		for feature in arrNomesFeatures:
			arr_obj_features.append(feature)
		return arr_obj_features
	#########################################################################
	def imprimirFeatures():
		for SubClass in FeatureFactory.__subclasses__():
			objFeatFact = None
			if(SubClass.IS_LANGUAGE_DEPENDENT):
				objFeatFact = SubClass(objEnglish)
			else:
				objFeatFact = SubClass()
			for feat in objFeatFact.createFeatures():
				print(feat.name)


	###################################################################
	#IF mmain
	import sys
	if(sys.argv[1] == "-L"):
		print("Lista de features:")	#printa a lista de features
		print(imprimirFeatures())
	else:
		arrNomesFeatures = func(sys.argv[1])
		#Dict=obtemObjetosFeatures(arrNomesFeatures)
