from feature.features import ReviewBasedFeature
import datetime
#TODO: Verificar pq está comentado e corrigir
'''class AgeReviewRatio(ReviewBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.first_review = float("inf")
        self.num_reviews = 0

    def checkReview(self,review):
        self.num_reviews += 1
        if(self.first_review > review.rev_timestamp):
            self.first_review = review.rev_timestamp

    @abstractmethod
    def compute_feature(self,last_review):
        first_review_date = datetime.datetime.fromtimestamp(self.first_review)
        age = (self.curr_date-first_review_date).days

        return age/self.num_reviews if self.num_reviews >0 else 0
'''
#TODO: Nas classes que não tivererm, colocar no inicio de cada classe sua descrição
#.....exemplo; ReviewCount
#ao inves de ser ThreeMonthProportionReview ser: NDaysProportionReview
#E fazer a proporção por dias, passados como paramtro
class ThreeMonthProportionReview(ReviewBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        #TODO: O nomde da variavel abaixo não está bom
        self.trreview = 0
        self.total_review = 0
    #TODO: Esses 90 são os 90 dias...Em vez dessa constante, deveria ser o numero de dias
    def checkReview(self,review):
        self.total_review += 1
        if((self.curr_date-datetime.datetime.fromtimestamp(review.rev_timestamp)).days < 90):
            self.trreview += 1

    def compute_feature(self,last_review):
        return self.trreview/self.total_review

    def finish_document(self,last_review):

        self.trreview = 0
        self.last_review = 0

#TODO: Melhorar o nome da classe
class ReviewModSize(ReviewBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.sizeref = 0

    #fazer parecido com o ThreeMonthProportionReview
    def checkReview(self,reference):
        self.sizeref = reference.rev_size

    def compute_feature(self,last_review):
        return (self.sizeref*100)/last_review.rev_size

    def finish_document(self,last_review):
        self.sizeref = 0


class PercentReviewsPerDay(ReviewBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.num_reviews = 0

    def checkReview(self,review):
        self.num_reviews += 1

    def compute_feature(self,reference):
        age = (self.curr_date-datetime.datetime.fromtimestamp(reference.rev_timestamp)).days
        ratio = self.num_reviews/float(age)
        return (ratio*100)/self.num_reviews

    def finish_document(self,review):
        self.num_reviews = 0

class ReviewOccasion(ReviewBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date,rev_name):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.rev_name = rev_name
        self.num_reviews = 0

    def checkReview(self,review):
        if(self.rev_name == review.reviewer_name):
            self.num_reviews += 1

    def compute_feature(self, last_review):
        if(self.num_reviews >= 4):
            self.num_reviews = 0

        return self.num_reviews
                num_users = self.dict_rev_per_user.keys()
                for user,qtd_rev in self.dict_rev_per_user.items():
                    if(qtd_rev<4):
                        int_ocasional += 1
                return int_ocasional/num_users
    def finish_document(self, review):
        self.num_reviews = 0


class ReviewCount(ReviewBasedFeature):
    '''Conta o numero de revisões de um artigo'''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.reviews = 0

    def checkReview(self,review):
        self.reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.reviews

class AnonymousReviewCount(Review):
    '''Conta o numero de revisões feita por usuarios anonimos'''
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.id_reviewer = int("inf")
        self.id_reviews = 0

    def checkReview(self, review):
        #checar por uma regexp se o name_reviewer é igual a um ip ou filtrar pelo review.int_rev_user_id (se for none, anonimo)
        if(type(sef.str_reviewer_name) != type(review.int_rev_id)):
            self.num_reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.num_reviews


class RegisteredReviewCount(Review):
    ''' Conta o numero de revisões feitas por usuarios registrados '''
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.id_reviewer = int("inf")
        self.num_reviews = 0

    def checkReview(self, review):
        if(type(self.id_reviewer) == type(review.int_rev_id)):
            self.num_reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.num_reviews

'''Desvio padrão da média de revisões feitas por usuários'''
class ReviewsPerUser(Review):
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        self.dict_rev_per_user = {};

    def checkReview(self, review):
        if(review.str_reviewer_name not in self.dict_rev_per_user):
            self.dict_rev_per_user[review.str_reviewer_name] = 0
        self.dict_rev_per_user[review.name_reviewer] += 1

    def compute_feature(self):
        devation = num_reviews_user**num_reviews_user
        devation = devation/num_reviews_user
        devation = math.sqrt(devation)
        return devation
