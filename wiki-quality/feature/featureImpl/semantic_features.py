import feature.features
import os
import nltk.data
from enum import Enum
from feature.features import TextBasedFeature

class POSTaggerTrainerFeature(TextBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,database,basedir,language,model):
        super(TextBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.basedir = basedir
        self.language = language
        self.model = model

    def compute_feature(self,document):
        return os.system(str("python3 " + self.basedir + "/train_tagger.py" + self.model))

    def finish_document(self,document):
        pass


class PartOfSpeechTaggerFeature(TextBasedFeature):

    MODELS = {"pt":"mac_morpho_aubt.pickle","en":"conll2000_aubt.pickle","es":"cess_esp_aubt.pickle"}

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,language):
        super(TextBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.language = language
        try:

            self.tagger = nltk.data.load(str("taggers/" + PartOfSpeechTaggerFeature.MODELS[self.language]))
        except LookupError:
            nltk.download(PartOfSpeechTaggerFeature.MODELS[self.language])
            #self.tagger = nltk.data.load(str("taggers/" + PartOfSpeechTaggerFeature.MODELS[self.language]))

    def compute_feature(self,document):
        return self.tagger.tag(word_tokenize(document))

    def finish_document(self,document):
        pass

class POSClassifierTrainerFeature(TextBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,database,basedir,language,mode,corpus,classifier):
        super(TextBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.basedir = basedir
        self.language = language
        self.corpus = corpus
        self.mode = mode
        self.classifier = classifier

    def compute_feature(self,document):
        return os.system(str("python3 " + self.basedir + "train_classifier.py " + self.corpus +
                             " --instance " + self.mode + " --classifier " + self.classifier))

    def finish_document(self,document):
        pass

class BagOfPOSFeature(PartOfSpeechTaggerFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(PartOfSpeechTaggerFeature).__init__(name, description, reference, visibility, text_format, feature_time_per_document, language)

    def compute_feature(self, document):
        feature = super(PartOfSpeechTaggerFeature).compute_feature(document)
        return {tag[1]:feature.count(tag[1]) for tag[1] in set(feature)}

    def finish_document(self, document):
        pass
