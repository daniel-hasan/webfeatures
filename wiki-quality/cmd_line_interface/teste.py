import unittest
import json
from .CaracterInterface import *
import os.path
import sys

#Autor: Gabriel Gonçalves, 2020 (gabrielgoncalves310503@gmail.com)


class TestCaracterInterface(unittest.TestCase):
    def testObtemObjetosFeatures(self):
        
        novoCaracterInterface = CaracterInterface()
        
        arrNomesFeatures = ["Section count","Subsection count", {"name":"Large phrase rate","param":{"Size threshold":2}}]
        
        arr_obj_features = novoCaracterInterface.obtemObjetosFeatures(arrNomesFeatures)
        
        self.assertEqual(len(arrNomesFeatures),len(arr_obj_features), "Erro! A lista de objetos de features não saiu como o esperado")

        ok = False
        for feat,nome in zip(arr_obj_features,arrNomesFeatures):
            ok=True
            
            if(type(nome) == dict):
                self.assertEqual(feat.name,nome["name"],"Erro! Nomes apresentam divergência")
            else:
                self.assertEqual(feat.name,nome,"Erro! Nomes apresentam divergência")
            
           
        self.assertTrue(ok,"Certifique-se que as listas não estejam vazias!")
        
    
    def testCaracterInterfaceFeaturesText(self):
        
        car = CaracterInterface()
        
        car.gera_arqtest()
        
        
        if(os.path.exists('cmd_line_interface/saida_anterior.json') and os.stat("cmd_line_interface/saida_anterior.json").st_size != 0):
            with open('cmd_line_interface/saida_anterior.json') as f:
                arquivoPreviamenteGerado = json.load(f)
                qtd_feat_ant = enumerate(arquivoPreviamenteGerado["header"])   
        else:
            arquivoPreviamenteGerado = open('cmd_line_interface/saida_anterior.json','w')
            
        
        arquivo_zip = "cmd_line_interface/zip.zip"
        nome_arquivo_saida_teste = "cmd_line_interface/saida_teste.json"
        arr_features = car.le_arquivo("cmd_line_interface/arqtest.json")
        formato = "textplain"
        saida_teste = car.execute(arquivo_zip, nome_arquivo_saida_teste, arr_features, formato)
        saida_teste = json.loads(json.dumps(saida_teste.data))
        
        arr_features = car.obtemObjetosFeatures(arr_features.get("arr_features"))
        arr_feat = enumerate(arr_features)
        
        
        if(os.stat("cmd_line_interface/saida_anterior.json").st_size == 0):
            saida_teste = open(nome_arquivo_saida_teste,"r")
            arquivoPreviamenteGerado.write(saida_teste.read())
            sys.exit()
            
        
        nome_textos_dentro_do_zip_antig = arquivoPreviamenteGerado["data"].keys()
        nome_textos_dentro_do_zip_antig = list(nome_textos_dentro_do_zip_antig)
        
        nome_textos_dentro_do_zip_atual = saida_teste["data"].keys()
        nome_textos_dentro_do_zip_atual = list(nome_textos_dentro_do_zip_atual)
        
        nome_textos_Dentro_do_zip_common = list(set(nome_textos_dentro_do_zip_antig).intersection(nome_textos_dentro_do_zip_atual))
        
        features_atuais = []
        for i, objFeature in arr_feat:
            features_atuais.append(saida_teste["header"].get(str(i)).get('name'))
        
        features_antigas = []
        for j, objFeatureAntiga in qtd_feat_ant:
            features_antigas.append(arquivoPreviamenteGerado["header"].get(str(j)).get('name'))
            
            
        features_comuns = []
        features_comuns = list(set(features_antigas).intersection(features_atuais))
        
        
        ok = True
        for text_common in nome_textos_Dentro_do_zip_common:
            
            resultado_antigo = arquivoPreviamenteGerado["data"].get(text_common)
            resultado_atual = saida_teste["data"].get(text_common)
            
            for feat_common in features_comuns:

                posic_antiga = features_antigas.index(feat_common)                    
                posic_nova = features_atuais.index(feat_common)
                
                self.assertEqual(resultado_antigo[posic_antiga],resultado_atual[posic_nova], "Erro! A feature '"+feat_common+"' calculada com base no arquivo '"+text_common+"' apresentou divergência de resultados")
                
                
                if(resultado_antigo[posic_antiga]==resultado_atual[posic_nova]):
                    ok = True
                else:
                    ok = False
                    sys.exit()
        
        
        if(ok == True):
            saida_anterior = open("cmd_line_interface/saida_anterior.json","w")
            saida_teste = open(nome_arquivo_saida_teste,"r")
            saida_anterior.write(saida_teste.read())
            saida_anterior.close()
            saida_teste.close()
            
            
            
    def testCaracterInterfaceFeaturesGraph(self):
        
        car = CaracterInterface()
        
        car.gera_arqtest_graph()
        
        if(os.path.exists("cmd_line_interface/graph_saida_anterior.json") and os.stat("cmd_line_interface/graph_saida_anterior.json").st_size != 0):
            
            with open("cmd_line_interface/graph_saida_anterior.json") as f:
                arquivoPreviamenteGerado = json.load(f)
                qtd_feat_ant = enumerate(arquivoPreviamenteGerado["header"])   
        else:
            arquivoPreviamenteGerado = open("cmd_line_interface/graph_saida_anterior.json",'w')
            
        
        arquivo_csv = "cmd_line_interface/teste_grafo.csv"
        nome_arquivo_saida_teste = "cmd_line_interface/graph_saida_teste.json"
        arr_features = car.le_arquivo("cmd_line_interface/graph_arqtest.json")
        formato = "graph"
        saida_teste = car.execute(arquivo_csv, nome_arquivo_saida_teste, arr_features, formato)
        saida_teste = json.loads(json.dumps(saida_teste.data))
        
        arr_features = car.obtemObjetosFeatures(arr_features.get("arr_features"))
        arr_feat = enumerate(arr_features)
        
        
        if(os.stat("cmd_line_interface/graph_saida_anterior.json").st_size == 0):
            saida_teste = open(nome_arquivo_saida_teste,"r")
            arquivoPreviamenteGerado.write(saida_teste.read())
            sys.exit()
        
        features_atuais = []
        for i, objFeature in arr_feat:
            features_atuais.append(saida_teste["header"].get(str(i)).get('name'))
        
        features_antigas = []
        for j, objFeatureAntiga in qtd_feat_ant:
            features_antigas.append(arquivoPreviamenteGerado["header"].get(str(j)).get('name'))
            
            
        features_comuns = []
        features_comuns = list(set(features_antigas).intersection(features_atuais))
        
        
        ok = True
        
        resultado_antigo = arquivoPreviamenteGerado["data"]
        resultado_atual = saida_teste["data"]
        
        for feat_common in features_comuns:
            
            posic_antiga = features_antigas.index(feat_common)                    
            posic_nova = features_atuais.index(feat_common)
            
            self.assertEqual(resultado_antigo[feat_common],resultado_atual[feat_common], "Erro! A feature "+feat_common+"apresentou divergência de resultados")
                
                
            if(resultado_antigo[feat_common]==resultado_atual[feat_common]):
                ok = True
            else:
                ok = False
                sys.exit()
        
        
        if(ok == True):
            saida_anterior = open("cmd_line_interface/graph_saida_anterior.json","w")
            saida_teste = open(nome_arquivo_saida_teste,"r")
            saida_anterior.write(saida_teste.read())
            saida_anterior.close()
            saida_teste.close()
        
        
                    
        
        
if __name__ == "__main__":
    unittest.main()
                
        
        
