
'''Conta o numero de revisões de um artigo'''
class ReviewCount(ReviewBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document)
        self.reviews = 0

    def checkReview(self,review):
        self.reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.reviews

'''Conta o numero de revisões feita por usuarios anonimos'''
class AnonymousReviewCount(ConfigurableParam):
    def __init__(self,att_name,name,description,default_value,param_type,arr_choices=[]):
        self.name_reviewer = string("inf")
        self.num_reviews = 0

    def checkReview(self, review):
        if(sef.name_reviewer == "null"):
            self.num_reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.num_reviews

''' Conta o numero de revisões feitas por usuarios registrados '''
class RegisteredReviewCount(ConfigurableParam):
    def __init__(self,att_name,name,description,default_value,param_type,arr_choices=[]):
        self.name_reviewer = string("inf")
        self.num_reviews = 0;

    def checkReview(self, review):
        if(self.name_reviewer != "null"):
            self.num_reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.num_reviews
