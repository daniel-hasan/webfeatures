import feature.features
import os
import nltk.data
import pickle
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

    MODELS = {"pt":"postag_models/pt_macmorpho_unigram.pickle","en":"postag_models/pt_macmorpho_unigram.pickle","es":"postag_models/pt_macmorpho_unigram.pickle"}

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,language):
        super(TextBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.BASE_DIR = os.path.abspath(os.path.join(self.BASE_DIR,os.pardir))

        self.language = language
        with open(f'{self.BASE_DIR}/{PartOfSpeechTaggerFeature.MODELS[self.language]}',"rb") as tag_file:
            self.tagger = pickle.load(tag_file)


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
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,language):
        super().__init__(name, description, reference, visibility, text_format, feature_time_per_document, language)

    def compute_feature(self, document):
        feature = super(PartOfSpeechTaggerFeature).compute_feature(document)
        return {tag[1]:feature.count(tag[1]) for tag[1] in set(feature)}

    def finish_document(self, document):
        pass
