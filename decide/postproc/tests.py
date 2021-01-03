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

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_paridad_1(self):
        data = {
            'type':'PARIDAD',
            'options': [
                {'option':'PSOE', 'number':1 , 'votes': 40, 'escanio': 4},
                {'option':'PACMA', 'number':2 , 'votes': 23, 'escanio': 4},
            ],
            'candidates': [
                {'id': '1', 'sex': 'H',  'edad':23},
                {'id': '2', 'sex': 'H',  'edad':42},
                {'id': '3', 'sex': 'M',  'edad':29},
                {'id': '4', 'sex': 'M',  'edad':26},
                {'id': '5', 'sex': 'H',  'edad':21},
                {'id': '6', 'sex': 'M',  'edad':22},
            ],
        }

        res = [
            {'option':'PSOE', 'number':1 , 'votes': 40, 'escanio': 4, 'paridad': [
                {'id': '3', 'sex': 'M', 'edad': 29}, 
                {'id': '1', 'sex': 'H', 'edad': 23}, 
                {'id': '4', 'sex': 'M', 'edad': 26}, 
                {'id': '2', 'sex': 'H', 'edad': 42}
                ]
            },
            {'option':'PACMA', 'number':2 , 'votes': 23, 'escanio': 4, 'paridad': [
                {'id': '3', 'sex': 'M', 'edad': 29}, 
                {'id': '1', 'sex': 'H', 'edad': 23}, 
                {'id': '4', 'sex': 'M', 'edad': 26}, 
                {'id': '2', 'sex': 'H', 'edad': 42}
                ]
            },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, res)

    def test_paridad_2(self):
        data = {
            'type':'PARIDAD',
            'options': [
                {'option':'PSOE', 'number':1 , 'votes': 240, 'escanio': 13},
                {'option':'PACMA', 'number':2 , 'votes': 123, 'escanio': 8},
                {'option':'PP', 'number':3 , 'votes': 233, 'escanio': 12},
            ],
            'candidates': [
                {'id': '1', 'sex': 'H',  'edad':23},
                {'id': '2', 'sex': 'H',  'edad':42},
                {'id': '3', 'sex': 'M',  'edad':29},
                {'id': '4', 'sex': 'H',  'edad':26},
                {'id': '5', 'sex': 'H',  'edad':21},
                {'id': '6', 'sex': 'M',  'edad':22},
                {'id': '7', 'sex': 'M',  'edad':28},
                {'id': '8', 'sex': 'H',  'edad':39},
                {'id': '9', 'sex': 'M',  'edad':19},
                {'id': '10', 'sex': 'M',  'edad':24},
                {'id': '11', 'sex': 'H',  'edad':27},
                {'id': '12', 'sex': 'M',  'edad':20},
            ],
        }
 
        res = [
            {'option': 'PSOE', 'number': 1, 'votes': 240, 'escanio': 13,'paridad': [
                {'id': '3', 'sex': 'M', 'edad': 29}, 
                {'id': '1', 'sex': 'H', 'edad': 23}, 
                {'id': '6', 'sex': 'M', 'edad': 22},
                {'id': '2', 'sex': 'H', 'edad': 42}, 
                {'id': '7', 'sex': 'M', 'edad': 28},
                {'id': '4', 'sex': 'H', 'edad': 26}, 
                {'id': '9', 'sex': 'M', 'edad': 19}, 
                {'id': '5', 'sex': 'H', 'edad': 21}, 
                {'id': '10', 'sex': 'M', 'edad': 24}, 
                {'id': '8', 'sex': 'H', 'edad': 39}, 
                {'id': '12', 'sex': 'M', 'edad': 20},
                {'id': '11', 'sex': 'H', 'edad': 27} 
                ]
            },
            {'option': 'PACMA', 'number': 2, 'votes': 123, 'escanio': 8, 'paridad': [
                {'id': '3', 'sex': 'M', 'edad': 29}, 
                {'id': '1', 'sex': 'H', 'edad': 23}, 
                {'id': '6', 'sex': 'M', 'edad': 22}, 
                {'id': '2', 'sex': 'H', 'edad': 42}, 
                {'id': '7', 'sex': 'M', 'edad': 28}, 
                {'id': '4', 'sex': 'H', 'edad': 26}, 
                {'id': '9', 'sex': 'M', 'edad': 19}, 
                {'id': '5', 'sex': 'H', 'edad': 21}
                ]
            },
            {'option': 'PP', 'number': 3, 'votes': 233, 'escanio': 12, 'paridad': [
                {'id': '3', 'sex': 'M', 'edad': 29}, 
                {'id': '1', 'sex': 'H', 'edad': 23}, 
                {'id': '6', 'sex': 'M', 'edad': 22},
                {'id': '2', 'sex': 'H', 'edad': 42}, 
                {'id': '7', 'sex': 'M', 'edad': 28},
                {'id': '4', 'sex': 'H', 'edad': 26}, 
                {'id': '9', 'sex': 'M', 'edad': 19}, 
                {'id': '5', 'sex': 'H', 'edad': 21}, 
                {'id': '10', 'sex': 'M', 'edad': 24}, 
                {'id': '8', 'sex': 'H', 'edad': 39}, 
                {'id': '12', 'sex': 'M', 'edad': 20},
                {'id': '11', 'sex': 'H', 'edad': 27} 
                ]}
        ]
        
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        
        values = response.json()
        print(values)

        
        