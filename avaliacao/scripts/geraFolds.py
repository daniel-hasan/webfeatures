import csv

lista = []
dicionario = {}

def write_svm_line(arrLinha,classLabel,f):
	intIdxFeature = 1
	f.write(classLabel)
	for col in arrLinha[1:]:
		f.write(" {idx}:{val}".format(idx=intIdxFeature,val=col))
		intIdxFeature += 1		

	f.write("\n")
with open('MV_results_wiki6.csv', 'r') as ficheiro:
	reader = list(csv.reader(ficheiro, delimiter=','))
	
	for linha in reader[1:]:
		fold=linha[0]
		if fold not in dicionario:
			dicionario[fold] = []
        	
		dicionario[fold].append(linha)

dicionarioFeat = {}
with open('resultDalip09-like.csv', 'r') as ficheiro:
	reader = list(csv.reader(ficheiro, delimiter=','))
	
	for linha in reader[1:]:
		pageId=linha[0]
		dicionarioFeat[pageId] = linha

for foldId,arrElementos in dicionario.items():
	#teste
	with open("teste.fold"+str(foldId)+".txt", 'w+') as arquivo:
		for linha in arrElementos:
			write_svm_line(dicionarioFeat[linha[1]],linha[3],arquivo)

	#treino
	with open("treino.fold"+str(foldId)+".txt", 'w+') as arquivo:
		for foldIdJ,arrElementosJ in dicionario.items():
			for linha in arrElementosJ:
				if foldIdJ != foldId:
					write_svm_line(dicionarioFeat[linha[1]],linha[3],arquivo)

