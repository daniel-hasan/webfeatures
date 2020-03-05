from CaracterInterface import *

def call_caracterInterface(self, arg, zipfile, result_datasetfile, format):
    	if(arg == "-L"):
    		print("Lista de features:")	#printa a lista de features
    		print(CaracterInterface.imprimirFeatures())
        else:

            arrNomesFeatures = CaracterInterface.obtemObjetosFeatures(CaracterInterface.le_arquivo(arg))
            CaracterInterface.execute(zipfile, result_datasetfile, arrNomesFeatures, format)
