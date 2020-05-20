import csv
import scipy.stats as stats

def le_info_gain(arquivo):
    arquivo = open(arquivo, 'r')
    dados = {}
    for linha in arquivo:
        while linha.find("  ") >= 0:
            linha = linha.replace("  ", " ")
        palavras = linha.split(" ")
       
        chave = palavras[3].replace("\n", "")
        if chave not in dados:
            dados[chave] = []
     
        dados[chave]=palavras[1]
    return dados

def le_dataset(arquivo):
    dados = {}
    with open(arquivo) as arquivocsv:
        ler = csv.DictReader(arquivocsv, delimiter=",")
        for linha in ler:
            for chave, valor in linha.items():
                if chave not in dados:
                    dados[chave] = []
                dados[chave].append(valor)
    return dados


def calcula_correlacao(dic_dataset_anterior, dic_dataset_webFeatures, dic_infogain):
    contadorAnterior = 0
    contadorAtual = 0
    maiorValor = -2
    indiceAtual = 0
    anterior = list(dic_dataset_anterior.keys())
    atual = list(dic_dataset_webFeatures.keys())
    infogain=list(dic_infogain.keys())
    temp=0
    result=[]
    while(contadorAnterior < len(dic_dataset_anterior)):
        contadorAtual = 0
        maiorValor = -2
        while(contadorAtual < len(dic_dataset_anterior)):
            tau, p_value = stats.spearmanr(list(dic_dataset_anterior[anterior[contadorAnterior]]), list(dic_dataset_webFeatures[atual[contadorAtual]]))
            if abs(tau) > maiorValor:
                maiorValor = abs(tau)
                maiorValorString = anterior[contadorAnterior]
                indiceAtual = contadorAtual
            contadorAtual = contadorAtual + 1
            for i in infogain:
              if(anterior[contadorAnterior]==i):
                temp = dic_infogain[i]
        result.append(anterior[contadorAnterior]+","+str(temp)+","+atual[indiceAtual]+","+str(maiorValor))
        print(result[contadorAnterior])
        contadorAnterior = contadorAnterior + 1
    return result

def organiza_ranking(dic_dataset):
    array_original = dic_dataset
    array_ordenado = []
    ranking = []
    contador = 0
    while(contador < len(array_original)):
        array_ordenado.append(array_original[contador])
        contador = contador + 1
    array_ordenado.sort()
    contador = 0
    while(contador < len(array_original)):
        contador2 = 0
        verificador = False
        while (contador2 < len(array_ordenado)):
            if(array_original[contador] == array_ordenado[contador2] and verificador == False):
                ranking.append(contador2)
                verificador = True
            contador2 = contador2 + 1
        contador = contador + 1
    return ranking

def criar_ranking(dic_dataset):
    keys = list(dic_dataset.keys())
    dic_ranking = {}
    array_atual = []
    array_organizado = []
    contador = 0
    while(contador < len(keys)):
        array_atual.clear()
        array_organizado.clear()
        array_atual = list(dic_dataset[keys[contador]])
        array_organizado = organiza_ranking(array_atual)
        dic_ranking[keys[contador]] = array_organizado
        contador = contador + 1
    return dic_ranking


def grava_resultado(result_correlacao, nome_arquivo):
    with open(nome_arquivo + '.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=" ",quotechar=' ',quoting=csv.QUOTE_MINIMAL)
        for i in result_correlacao:
            spamwriter.writerow(i)
    print("Arquivo criado")


dic_anterior = le_dataset('data_wikiText_dalip2009.csv')
dic_web_features = le_dataset('data_wikiWebFeatures.csv')
info_gain = le_info_gain('info_gain_dalip2009.txt')

dic_anterior_ranking = criar_ranking(dic_anterior)
dic_web_features_ranking = criar_ranking(dic_web_features)
info_gain_ranking = criar_ranking(info_gain)

result_correlacao = calcula_correlacao(dic_anterior, dic_web_features, info_gain)
result_correlacao_ranking = calcula_correlacao(dic_anterior_ranking, dic_web_features_ranking, info_gain_ranking)

grava_resultado(result_correlacao, "resultado")
grava_resultado(result_correlacao, "resultado_ranking")
