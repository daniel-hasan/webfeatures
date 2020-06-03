import json
#from feature.features import FeatureDocumentsReader, FeatureDocumentsWriter, FeatureCalculator
#from feature.features import
#from utils.uncompress_data import CompressedFile

import unittest
from .CaracterInterface import * #importamos



#teste
class TestCaracterInterface(unittest.TestCase):
    def testObtemObjetosFeatures(self):
        
        novoCaracterInterface = CaracterInterface()
        
        arrNomesFeatures = ["Section count","Subsection count","Complete URL link count"]
        
        arr_obj_features = novoCaracterInterface.obtemObjetosFeatures(arrNomesFeatures)
        
        self.assertEqual(len(arrNomesFeatures),len(arr_obj_features), "Erro! A lista de objetos de features não saiu como o esperado")

        ok = False
        for feat,nome in zip(arr_obj_features,arrNomesFeatures):
            ok=True
            self.assertEqual(feat.name,nome,"Erro! Nomes apresentam divergência")
           
        self.assertTrue(ok,"Certifique-se que as listas não estejam vazias!")
        
    
    def testCaracterInterface(self):
        
        car = CaracterInterface()
        
        """Abre o arquivo que foi gerado pela CaracterInterface em outra ocasião no passado onde, provavelmente, não havia sido incluidas todas as features que atualmente estão implementadas; Nesta ocasião do passado, poderia, também, haver arquivos de texto no zip que já não existem no presente momento ou podem ter sido inseridos novos arquivos, além dos que já existiam. Os que não existiam quando este arquivo foi gerado obviamente não tiveram suas características calculadas pelas features. O nosso teste só leva em conta os resultados referentes a textos que existiam quando o arquivo prévio foi gerado e que continuam existindo atualmente (ou seja, os textos que os dois arquivos de saída (o previamente gerado e o gerado neste presente código) possuem em comum. Também só leva em conta features existentes quando os dois arquivos foram gerados. Mês passado, por exemplo, existia a feature X que, calculada com base no meu texto a.txt, me deu o resultado 8. Atualmente, essa feature não existe mais, foi excluida. Portanto, não irá gerar mais nenhum resultado. Essa situação passará perfeitamente pelo teste sem que gere erros. O teste só irá comparar os resultados obtidos pela mesma feature presente nos dois arquivos, independentemente se novas features foram implementadas ou entraram em desuso"""
        
        with open('cmd_line_interface/out.json') as f:    
            arquivoPreviamenteGerado = json.load(f)
        qtd_feat_ant = enumerate(arquivoPreviamenteGerado["header"])
        
        arquivo_zip = "cmd_line_interface/zip.zip"
        nome_arquivo_saida_teste = "cmd_line_interface/saida_teste.json"
        arr_features = car.le_arquivo("cmd_line_interface/arqtest.json")
        formato = "textplain"
        saida = car.execute(arquivo_zip, nome_arquivo_saida_teste, arr_features, formato)
        saida = json.loads(json.dumps(saida.data))
        
        arr_features = car.obtemObjetosFeatures(arr_features.get("arr_features"))
        arr_feat = enumerate(arr_features)
        
        
        
        nome_textos_dentro_do_zip_antig = arquivoPreviamenteGerado["data"].keys()
        nome_textos_dentro_do_zip_antig = list(nome_textos_dentro_do_zip_antig)
        
        nome_textos_dentro_do_zip_atual = saida["data"].keys()
        nome_textos_dentro_do_zip_atual = list(nome_textos_dentro_do_zip_atual)
        
        nome_textos_Dentro_do_zip_common = list(set(nome_textos_dentro_do_zip_antig).intersection(nome_textos_dentro_do_zip_atual))
        
        features_atuais = []
        for i, objFeature in arr_feat:
            features_atuais.append(saida["header"].get(str(i)).get('name'))
        
        features_antigas = []
        for j, objFeatureAntiga in qtd_feat_ant:
            features_antigas.append(arquivoPreviamenteGerado["header"].get(str(j)).get('name'))
            
            
        features_comuns = []
        features_comuns = list(set(features_antigas).intersection(features_atuais))
        
        for text_common in nome_textos_Dentro_do_zip_common:
            
            resultado_antigo = arquivoPreviamenteGerado["data"].get(text_common)
            resultado_atual = saida["data"].get(text_common)
            
            for feat_common in features_comuns:

                posic_antiga = features_antigas.index(feat_common)                    
                posic_nova = features_atuais.index(feat_common)
                
                self.assertEqual(resultado_antigo[posic_antiga],resultado_atual[posic_nova], "Erro! A feature '"+feat_common+"' calculada com base no arquivo '"+text_common+"' apresentou divergência de resultados")
        
        
if __name__ == "__main__":
    unittest.main()
                
        
        
