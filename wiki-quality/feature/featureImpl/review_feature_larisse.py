
class ReviewCount(ReviewBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document)
        self.date_article = float("inf")

    @abstractmethod
    def compute_feature(self,):
        date_article = datetime.datetime.fromtimestamp(self.date_article)
        age = (self.curr_date-date_article).days

        return age
