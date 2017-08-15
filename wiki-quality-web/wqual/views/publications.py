'''
Created on 14 de ago de 2017

@author: profhasan
'''
from django.views.generic.list import ListView

from wqual.models import Publication


class PublicationList(ListView):
    #filtrar por usuario logado
    model = Publication
    template_name = "content/publication_list.html"