from .CaracterInterface import *

def call_caracterInterface(self, arg, zipfile, result_datasetfile, format):
<<<<<<< HEAD
    	if(arg == "-L"):
    		print("Lista de features:")	#printa a lista de features
            car = CaracterInterface()
    		print(car.imprimirFeatures())
        else:

            arrNomesFeatures = CaracterInterface.obtemObjetosFeatures(CaracterInterface.le_arquivo(arg))
            CaracterInterface.execute(zipfile, result_datasetfile, arrNomesFeatures, format)
=======
    if(arg == "-L"):
        print("Lista de features:")	#printa a lista de features
        car = CaracterInterface()
        print(car.imprimirFeatures())
    else:
        arrNomesFeatures = CaracterInterface.obtemObjetosFeatures(CaracterInterface.le_arquivo(arg))
        CaracterInterface.execute(zipfile, result_datasetfile, arrNomesFeatures, format)
>>>>>>> 8179693eab3a24feca475f027b767578b3037e3a
