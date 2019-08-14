import json
from feature.features import Document as DocumentFeature
from utils.uncompress_data import CompressedFile

class DatasetDocReader(FeatureDocumentsReader):

    def __init__(self, dataset):
        self.dataset = dataset

    def get_zip_to_doc_feature(self, file):
        int_total_file_size = 0
        file_zip = CompressedFile.get_compressed_file(file)
        int_file_size = list(file_zip.get_each_file_size())
        i = 0
        for name,strFileTxt in file_zip.read_each_file():

            objDocumento = Document(nam_file=name, dataset=self, num_file_size = int_file_size[i][1])
            int_total_file_size += int_file_size[i][1]
            i = i+1

            yield DocumentFeature(objDocumento.id,objDocumento.nam_file,str(strFileTxt))


    def get_documents(self):

        sub_dataset = SubmittedDataset.objects.filter(dataset=self.dataset)[0]

        for doc in sub_dataset.dataset.get_zip_to_doc_feature(sub_dataset.file):
                yield doc



class DatasetDocWriter(FeatureDocumentsWriter):
        def __init__(self, dataset):
            self.dataset = dataset

        def write_header(self,arr_features):
            dictFeatureHeader = {}
			arr_feat = enumerate(arr_features)
            for i,objFeature in arr_feat:
				instances = []
                dictFeatureHeader[i] = {"header":{"name":objFeature.name,
                                        "params":objFeature.get_params_str()},"instances":{str(arr_feat):instances.append(i)}

            self.dataset.dsc_result_header = dictFeatureHeader

        def write_document(self,document, arr_feats_used, arr_feats_result):
            self.document = document
            self.arr_feats_used = arr_feats_used

            self.arr_feats_result = arr_feats_result

            doc=DocumentDataset.objects.get(id = self.document.int_doc_id)
            doc_result = DocumentResult(dsc_result=self.arr_feats_result, document=doc)
            doc_result.save()



class Document(models.Model):
    '''
    Created on 14 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Cada documento contido no dataset que o usuário enviou
    '''

    nam_file = models.CharField(max_length=255, blank=True, null=True)
    dataset = models.ForeignKey(Dataset, models.CASCADE)
    num_file_size = models.IntegerField(blank=True, null=True)

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


'''
	# Implemenar um datasertfile reader
	# Implenmentar o docReader
	# implementar o docwriter
	{"header":{"name":objFeature.name,
	           "params":objFeature.get_params_str()},
	"instances":{"12":[12,31,213,12'],"1312":[]}
	}
	. Criar um metodo a mais no doc writer (pai):
	finishAllDocuments(self):
		pass
	No docWriter que estamos criando: salvar o arquivo
	#No feature calculator: chaamr o finishAllDocuments quando terminar
	#rodar o feature calculator

	#
'''
