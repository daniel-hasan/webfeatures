from django.test import TestCase
from django.test.client import Client
from django.urls.base import reverse
from plainbox.testing_utils import testcases


# Create your tests here.
class UrlName(object):
    def __init__(self,str_name,arr_args=[]):
        self.str_name = str_name
        self.arr_args = arr_args
        
class HomePageOpenTest(TestCase):
    ARR_URL_NAMES_ARGS = [UrlName("feature_set_list")]
    
    
    
    def test_status_code_200(self):
        for obj_url in HomePageOpenTest.ARR_URL_NAMES_ARGS:
            str_url = reverse(obj_url.str_name,args=obj_url.arr_args)
            #print("URL>>>>>>>>>>>> "+str_url)
            c = Client()
            response = c.get(str_url)
            self.assertEqual(response.status_code, 200, 
                             "A url de nome {name} ({url}) retornou o status code {status}".format(name=obj_url.str_name,url=str_url,status=response.status_code))
            
            
