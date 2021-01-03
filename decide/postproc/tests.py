from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    
    
    def test_paridad_3(self):
        data = {
            'type':'PARIDAD',
            'options': [
                {'option':'PSOE', 'number':1 , 'votes': 40, 'escanio': 4,'candidates': [
                {'id': '1', 'sex': 'H',  'edad':23},
                {'id': '2', 'sex': 'H',  'edad':42},
                {'id': '3', 'sex': 'H',  'edad':29},
                {'id': '4', 'sex': 'H',  'edad':26},
                {'id': '5', 'sex': 'H',  'edad':21},
                {'id': '6', 'sex': 'H',  'edad':22},
            ]},
                {'option':'PACMA', 'number':2 , 'votes': 23, 'escanio': 4,'candidates': [
                {'id': '1', 'sex': 'H',  'edad':23},
                {'id': '2', 'sex': 'H',  'edad':42},
                {'id': '3', 'sex': 'H',  'edad':29},
                {'id': '4', 'sex': 'H',  'edad':26},
                {'id': '5', 'sex': 'H',  'edad':21},
                {'id': '6', 'sex': 'H',  'edad':22},
            ]},
            ]
        }
        
        expected_result = {'message' : 'la diferencia del numero de hombres y mujeres es de más de un 60% - 40%'}
        response = self.client.post('/postproc/', data, format='json')
     
        self.assertEqual(response.status_code, 200)
                
        values = response.json()
       
        self.assertEqual(values, expected_result)