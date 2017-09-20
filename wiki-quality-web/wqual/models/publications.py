# -*- coding: utf-8 -*-
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
    nam_first = models.CharField(max_length=50)
    nam_middle = models.CharField(max_length=50)
    nam_last = models.CharField(max_length=50)

    def __str__(self):
        return "{first_name} {middle_name} {last_name}".format(first_name=self.nam_first,middle_name=self.nam_middle,last_name=self.nam_last)
    
class Conference(models.Model):
    '''
            Created on 13 de ago de 2017

            @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br> 
            Conferência/congresso (ou revista) de onde a publicação foi feita..
    '''
    nam_conference = models.CharField(max_length=255)
    nam_abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return "{name} ({abbr})".format(name=self.nam_conference,abbr=self.nam_abbreviation)
    
class Publication(models.Model):
    '''
            Created on 13 de ago de 2017
            @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br> 
            Representa uma publicação (qualquer tipo de artigo, sem distingui-los - a princípio).
    '''
    nam_title = models.CharField(max_length=400)
    num_year = models.IntegerField()
    
    authors = models.ManyToManyField(Author)
    conference = models.ForeignKey(Conference, models.PROTECT)
    
    def __str__(self):
        arr_str_authors = [str(author) for author in self.authors.all()]
        return "{authors}. {title}: {conference} ({year})".format(title=self.nam_title,
                                                                   year=str(self.num_year),
                                                                   conference=self.conference.nam_abbreviation,
                                                                   authors=" ;".join(arr_str_authors)
                                                                   )
