'''
Created on 21 de ago de 2017

@author: profhasan
'''
from wiki_quality_web.settings.development import *

DATABASES['default']['TEST']['NAME'] = 'wiki_quality'
DATABASES['default']['USER'] = 'root'