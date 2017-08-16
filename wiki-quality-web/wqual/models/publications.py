'''
Created on 13 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Tabelas responsáveis por armazenar a lista de publicação dos membros do grupo relacionadas ao projeto wikiQuality.
'''
from django.db import models

    
class Author(models.Model):
    '''
            Created on 13 de ago de 2017
            @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
            Autor da publicação. 
    '''
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return "{first_name} {middle_name} {last_name}".format(first_name=self.first_name,middle_name=middle_name,last_name=self.last_name)
    
class Conference(models.Model):
    '''
            Created on 13 de ago de 2017

            @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br> 
            Conferência/congresso (ou revista) de onde a publicação foi feita..
    '''
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return "{name} ({abbr})".format(name=self.name,abbr=self.abbreviation)
    
class Publication(models.Model):
    '''
            Created on 13 de ago de 2017
            @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br> 
            Representa uma publicação (qualquer tipo de artigo, sem distingui-los - a princípio).
    '''
    title = models.CharField(max_length=400)
    year = models.IntegerField()
    
    authors = models.ManyToManyField(Author)
    conference = models.ForeignKey(Conference, models.PROTECT)
    
    def __str__(self):
        arr_str_authors = [str(author) for author in self.authors.all()]
        return "{authors}. {title}: {conference} ({year})".format(title=self.title,
                                                                   year=str(self.year),
                                                                   conference=self.conference.abbreviation,
                                                                   authors=" ;".join(arr_str_authors)
                                                                   )
