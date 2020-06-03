from cmd_line_interface.CaracterInterface import *


def geraArrFeatName_SemImpressao():
        
        arr_feat_name = []
        arr_feature_factories = []
        objEnglish = LanguageEnum.en
        for SubClass in FeatureFactory.__subclasses__(): #percorre todas as features
            objFeatFact = None
            if(SubClass.IS_LANGUAGE_DEPENDENT):
                objFeatFact = SubClass(objEnglish)# instancia as features de acordo com o idioma
            else:
                objFeatFact = SubClass()
            arr_feature_factories.append(objFeatFact)

        for objFeatFact in arr_feature_factories:
            for feat in objFeatFact.createFeatures():
                arr_feat_name.append(feat.name) #adiciona o nome das features no vetor arr
                
        arr_feat_name.sort()
        return arr_feat_name

lista_features = geraArrFeatName_SemImpressao()

conteudo_arquivo_json = {}
conteudo_arquivo_json["arr_features"] = lista_features
conteudo_arquivo_json = json.dumps(conteudo_arquivo_json)

arquivo_json = open("cmd_line_interface/arqtest2.json","w")
arquivo_json.write(conteudo_arquivo_json)