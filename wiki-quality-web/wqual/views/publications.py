'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a visualização das publicações
'''
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from wqual.models import Publication


class PublicationList(LoginRequiredMixin, ListView):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lista todas as publicações
    '''
    
    model = Publication
    template_name = "content/publication_list.html"