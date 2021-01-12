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
        


    def test_genero_1(self):
        data = {
            'type':'PARIDAD',
            'options': [
                {'option':'PSOE', 'number':1 , 'votes': 40, 'escanio': 4},
                {'option':'PACMA', 'number':2 , 'votes': 23, 'escanio': 4},
            ],
            'candidates': [
                {'id': '1', 'sex': 'M',  'edad':23},
                {'id': '2', 'sex': 'M',  'edad':42},
                {'id': '3', 'sex': 'M',  'edad':29},
                {'id': '4', 'sex': 'M',  'edad':26},
                {'id': '5', 'sex': 'M',  'edad':21},
                {'id': '6', 'sex': 'H',  'edad':22},
            ],
        }

        res = [
            {'option':'PSOE', 'number':1 , 'votes': 40, 'escanio': 4, 'paridad': [
                {'id': '3', 'sex': 'M', 'edad': 29}, 
                {'id': '1', 'sex': 'M', 'edad': 23}, 
                {'id': '4', 'sex': 'M', 'edad': 26}, 
                {'id': '2', 'sex': 'H', 'edad': 42}
                ]
            },
            {'option':'PACMA', 'number':2 , 'votes': 23, 'escanio': 4, 'paridad': [
                {'id': '3', 'sex': 'M', 'edad': 29}, 
                {'id': '1', 'sex': 'M', 'edad': 23}, 
                {'id': '4', 'sex': 'M', 'edad': 26}, 
                {'id': '2', 'sex': 'H', 'edad': 42}
                ]
            },
        ]

        
        result = {'message' : 'la diferencia del numero de hombres y mujeres es de más de un 60% - 40%'}
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
                
        values = response.json()
        self.assertEqual(values, result)
        
    def test_genero_2(self):
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
                {'id': '6', 'sex': 'H',  'edad':22},
            ],
        }

        res = [
            {'option':'PSOE', 'number':1 , 'votes': 40, 'escanio': 4, 'paridad': [
                {'id': '3', 'sex': 'H', 'edad': 29}, 
                {'id': '1', 'sex': 'H', 'edad': 23}, 
                {'id': '4', 'sex': 'M', 'edad': 26}, 
                {'id': '2', 'sex': 'H', 'edad': 42}
                ]
            },
            {'option':'PACMA', 'number':2 , 'votes': 23, 'escanio': 4, 'paridad': [
                {'id': '3', 'sex': 'H', 'edad': 29}, 
                {'id': '1', 'sex': 'H', 'edad': 23}, 
                {'id': '4', 'sex': 'M', 'edad': 26}, 
                {'id': '2', 'sex': 'H', 'edad': 42}
                ]
            },
        ]

        
        result = {'message' : 'la diferencia del numero de hombres y mujeres es de más de un 60% - 40%'}
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
                
        values = response.json()
        self.assertEqual(values, result)
    def test_genero_3(self):
        data = {
            'type':'PARIDAD',
            'options': [
                {'option':'PACMA', 'number':1 , 'votes': 40, 'escanio': 4},
                {'option':'PSOE', 'number':2 , 'votes': 23, 'escanio': 4},
            ],
            'candidates': [
                {'id': '1', 'sex': 'H',  'edad':23},
                {'id': '2', 'sex': 'M',  'edad':42},
                {'id': '3', 'sex': 'M',  'edad':29},
                {'id': '4', 'sex': 'M',  'edad':26},
                {'id': '5', 'sex': 'M',  'edad':21},
                {'id': '6', 'sex': 'M',  'edad':22},
            ],
        }

        res = [
            {'option':'PSOE', 'number':1 , 'votes': 40, 'escanio': 4, 'paridad': [
                {'id': '3', 'sex': 'H', 'edad': 29}, 
                {'id': '1', 'sex': 'H', 'edad': 23}, 
                {'id': '4', 'sex': 'H', 'edad': 26}, 
                {'id': '2', 'sex': 'H', 'edad': 42}
                ]
            },
            {'option':'PACMA', 'number':2 , 'votes': 23, 'escanio': 4, 'paridad': [
                {'id': '3', 'sex': 'H', 'edad': 29}, 
                {'id': '1', 'sex': 'H', 'edad': 23}, 
                {'id': '4', 'sex': 'H', 'edad': 26}, 
                {'id': '2', 'sex': 'H', 'edad': 42}
                ]
            },
        ]

        
        result = {'message' : 'la diferencia del numero de hombres y mujeres es de más de un 60% - 40%'}
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
                
        values = response.json()
        self.assertEqual(values, result)


    def test_simple(self):
        data = {
            'type': 'SIMPLE',
            'escanio': 7,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 }, 
                { 'option': 'Option 2', 'number': 2, 'votes': 2 },
                { 'option': 'Option 3', 'number': 3, 'votes': 5 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        } 
        
        expect_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 5, 'postproc': 2 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 2 },
            { 'option': 'Option 2', 'number': 2, 'votes': 2, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 0 },
            ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expect_result)
    
    def test_simple1(self):
        data = {
            'type': 'SIMPLE',
            'escanio':40,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 10 },
                { 'option': 'Option 2', 'number': 2, 'votes': 8 },
                { 'option': 'Option 3', 'number': 3, 'votes': 1 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 4 },
                { 'option': 'Option 6', 'number': 6, 'votes': 5 },
            ]
        }
        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 13 },
            { 'option': 'Option 2', 'number': 2, 'votes': 8, 'postproc': 11 },
            { 'option': 'Option 6', 'number': 6, 'votes': 5, 'postproc': 7 },
            { 'option': 'Option 5', 'number': 5, 'votes': 4, 'postproc': 5 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 3 },
            { 'option': 'Option 3', 'number': 3, 'votes': 1, 'postproc': 1 },
        ]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_mgu_un_gandor(self):
        data = {
            'type': 'MGU',
            'escanio': 10,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 7 },
                { 'option': 'Option 2', 'number': 2, 'votes': 4 },
                { 'option': 'Option 3', 'number': 3, 'votes': 19 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 10 },
                { 'option': 'Option 6', 'number': 6, 'votes': 9 },

            ]
        }
        expected_result = [
            { 'option': 'Option 3', 'number': 3, 'votes': 19, 'postproc': 10 },
            { 'option': 'Option 5', 'number': 5, 'votes': 10, 'postproc': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 9, 'postproc': 0 },
            { 'option': 'Option 1', 'number': 1, 'votes': 7, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 4, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2 , 'postproc': 0 }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    

    def test_mgu_varios_ganadores_reparto_equitativo(self):
        data = {
            'type': 'MGU',
            'escanio': 20,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 6 },
                { 'option': 'Option 2', 'number': 2, 'votes': 5 },
                { 'option': 'Option 3', 'number': 3, 'votes': 10 },
                { 'option': 'Option 4', 'number': 4, 'votes': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 10 },
                { 'option': 'Option 6', 'number': 6, 'votes': 9 },
            ]
        }

        expected_result = [
            { 'option': 'Option 3', 'number': 3, 'votes': 10, 'postproc': 10 },
            { 'option': 'Option 5', 'number': 5, 'votes': 10, 'postproc': 10 },
            { 'option': 'Option 6', 'number': 6, 'votes': 9, 'postproc': 0 },
            { 'option': 'Option 1', 'number': 1, 'votes': 6, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 5, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 0 , 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple2(self):
        data = {
            'type': 'SIMPLE',
            'escanio':70,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 50 },
                { 'option': 'Option 2', 'number': 2, 'votes': 11 },
                { 'option': 'Option 3', 'number': 3, 'votes': 10},
                { 'option': 'Option 4', 'number': 4, 'votes': 1 },
                { 'option': 'Option 5', 'number': 5, 'votes': 6 },
                { 'option': 'Option 6', 'number': 6, 'votes': 4 },
            ]
        }
        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 50, 'postproc':  43},
            { 'option': 'Option 2', 'number': 2, 'votes': 11, 'postproc':  9},
            { 'option': 'Option 3', 'number': 3, 'votes': 10, 'postproc': 9},
            { 'option': 'Option 5', 'number': 5, 'votes': 6, 'postproc': 5},
            { 'option': 'Option 6', 'number': 6, 'votes': 4, 'postproc': 3},
            { 'option': 'Option 4', 'number': 4, 'votes': 1, 'postproc': 1},
        ]
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple3(self):
        data = {
            'type': 'SIMPLE',
            'escanio':100,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 40 },
                { 'option': 'Option 2', 'number': 2, 'votes': 30 },
                { 'option': 'Option 3', 'number': 3, 'votes': 1},
                { 'option': 'Option 4', 'number': 4, 'votes': 14},
                { 'option': 'Option 5', 'number': 5, 'votes': 2 },
                { 'option': 'Option 6', 'number': 6, 'votes': 15 },
            ]
        }
        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 40, 'postproc':  39},
            { 'option': 'Option 2', 'number': 2, 'votes': 30, 'postproc':  29},
            { 'option': 'Option 6', 'number': 6, 'votes': 15, 'postproc': 15},
            { 'option': 'Option 4', 'number': 4, 'votes': 14, 'postproc': 14},
            { 'option': 'Option 5', 'number': 5, 'votes': 2, 'postproc': 2},
            { 'option': 'Option 3', 'number': 3, 'votes': 1, 'postproc': 1},
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple4(self):
        data = {
            'type': 'SIMPLE',
            'escanio':20,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 3 },
                { 'option': 'Option 3', 'number': 3, 'votes': 1},
                { 'option': 'Option 4', 'number': 4, 'votes': 4},
                { 'option': 'Option 5', 'number': 5, 'votes': 2 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }
        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc':  6},
            { 'option': 'Option 4', 'number': 4, 'votes': 4, 'postproc':  5},
            { 'option': 'Option 2', 'number': 2, 'votes': 3, 'postproc': 4},
            { 'option': 'Option 5', 'number': 5, 'votes': 2, 'postproc': 3},
            { 'option': 'Option 3', 'number': 3, 'votes': 1, 'postproc': 1},
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1},
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple5(self):
        data = {
            'type': 'SIMPLE',
            'escanio':30,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 15 },
                { 'option': 'Option 2', 'number': 2, 'votes': 10 },
                { 'option': 'Option 3', 'number': 3, 'votes': 14},
                { 'option': 'Option 4', 'number': 4, 'votes': 5},
                { 'option': 'Option 5', 'number': 5, 'votes': 2 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1},
            ]
        }
        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 15, 'postproc':  10},
            { 'option': 'Option 3', 'number': 3, 'votes': 14, 'postproc':  9},
            { 'option': 'Option 2', 'number': 2, 'votes': 10, 'postproc': 6},
            { 'option': 'Option 4', 'number': 4, 'votes': 5, 'postproc': 3},
            { 'option': 'Option 5', 'number': 5, 'votes': 2, 'postproc': 1},
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1},
        ]
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_mgu_varios_ganadores_reparto_no_equitativo(self):
        data = {
            'type': 'MGU',
            'escanio': 32,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 6 },
                { 'option': 'Option 2', 'number': 2, 'votes': 5 },
                { 'option': 'Option 3', 'number': 3, 'votes': 15 },
                { 'option': 'Option 4', 'number': 4, 'votes': 15 },
                { 'option': 'Option 5', 'number': 5, 'votes': 15 },
                { 'option': 'Option 6', 'number': 6, 'votes': 9 },
            ]
        }
        expected_result = [
            { 'option': 'Option 3', 'number': 3, 'votes': 15, 'postproc': 10 },
            { 'option': 'Option 4', 'number': 4, 'votes': 15 , 'postproc': 10 },
            { 'option': 'Option 5', 'number': 5, 'votes': 15, 'postproc': 10 },
            { 'option': 'Option 6', 'number': 6, 'votes': 9, 'postproc': 2 },
            { 'option': 'Option 1', 'number': 1, 'votes': 6, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 5, 'postproc': 0 },
        ]
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    
    

    def test_mgu_todos_ganadores(self):
        data = {
            'type': 'MGU',
            'escanio': 15,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 8 },
                { 'option': 'Option 2', 'number': 2, 'votes': 8 },
                { 'option': 'Option 3', 'number': 3, 'votes': 8 },
                { 'option': 'Option 4', 'number': 4, 'votes': 8 },
                { 'option': 'Option 5', 'number': 5, 'votes': 8 },
                { 'option': 'Option 6', 'number': 6, 'votes': 8 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 8, 'postproc': 5 },
            { 'option': 'Option 2', 'number': 2, 'votes': 8 , 'postproc': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 8, 'postproc': 2 },
            { 'option': 'Option 4', 'number': 4, 'votes': 8, 'postproc': 2 },
            { 'option': 'Option 5', 'number': 5, 'votes': 8, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 8, 'postproc': 2 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    
    def test_mgu_mas_ganadores_que_seats(self):
        data = {
            'type': 'MGU',
            'escanio': 5,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 8 },
                { 'option': 'Option 2', 'number': 2, 'votes': 8 },
                { 'option': 'Option 3', 'number': 3, 'votes': 8 },
                { 'option': 'Option 4', 'number': 4, 'votes': 8 },
                { 'option': 'Option 5', 'number': 5, 'votes': 8 },
                { 'option': 'Option 6', 'number': 6, 'votes': 8 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 8, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 8 , 'postproc': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 8, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 8, 'postproc': 1 },
            { 'option': 'Option 5', 'number': 5, 'votes': 8, 'postproc': 1 },
            { 'option': 'Option 6', 'number': 6, 'votes': 8, 'postproc': 0 },
        ]
       
       
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    
    
    def test_mgu_varios_ganadores_reparto_no_equitativo2(self):
        data = {
            'type': 'MGU',
            'escanio': 43,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 6 },
                { 'option': 'Option 2', 'number': 2, 'votes': 5 },
                { 'option': 'Option 3', 'number': 3, 'votes': 15 },
                { 'option': 'Option 4', 'number': 4, 'votes': 15 },
                { 'option': 'Option 5', 'number': 5, 'votes': 15 },
                { 'option': 'Option 6', 'number': 6, 'votes': 15 },
            ]
        }

        expected_result = [
            { 'option': 'Option 3', 'number': 3, 'votes': 15, 'postproc': 10 },
            { 'option': 'Option 4', 'number': 4, 'votes': 15 , 'postproc': 10 },
            { 'option': 'Option 5', 'number': 5, 'votes': 15, 'postproc': 10 },
            { 'option': 'Option 6', 'number': 6, 'votes': 15, 'postproc': 10 },
            { 'option': 'Option 1', 'number': 1, 'votes': 6, 'postproc': 3 },
            { 'option': 'Option 2', 'number': 2, 'votes': 5, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    # Test con valores correctos
    def test_dhondtParidad(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 100000},
                {'option': 'Option 2', 'number': 2, 'votes': 75000},
                {'option': 'Option 3', 'number': 3, 'votes': 50000},
                {'option': 'Option 4', 'number': 4, 'votes': 25000},
            ],
            'escanio': 5,
            'candidates': [
                {'id': '1', 'sex': 'H',  'edad':23},
                {'id': '2', 'sex': 'H',  'edad':42},
                {'id': '3', 'sex': 'M',  'edad':29},
                {'id': '4', 'sex': 'M',  'edad':26},
                {'id': '5', 'sex': 'H',  'edad':21},
                {'id': '6', 'sex': 'M',  'edad':22},]
        }

        expected_result1 = [
            {'option': 'Option 1', 'number': 1, 'votes': 100000, 'escanio': 2, 'paridad':[
                                                        {'id': '3', 'sex': 'M', 'edad': 29}, 
                                                        {'id': '1', 'sex': 'H', 'edad': 23}]},
            {'option': 'Option 2', 'number': 2, 'votes': 75000, 'escanio': 2, 'paridad': [
                                                        {'id': '3', 'sex': 'M', 'edad': 29}, 
                                                        {'id': '1', 'sex': 'H', 'edad': 23}]},
            {'option': 'Option 3', 'number': 3, 'votes': 50000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
            {'option': 'Option 4', 'number': 4, 'votes': 25000, 'escanio': 0, 'paridad' : []},
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result1)

    def test_dhondtParidad1(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 300000},
                {'option': 'Option 2', 'number': 2, 'votes': 750000},
                {'option': 'Option 3', 'number': 3, 'votes': 500000},
                {'option': 'Option 4', 'number': 4, 'votes': 250000},
                {'option': 'Option 5', 'number': 5, 'votes': 250000},
                {'option': 'Option 6', 'number': 6, 'votes': 250000},
                  
            ],
            'escanio': 15,
            'candidates': [
                {'id': '1',  'sex': 'H',  'edad':23},
                {'id': '2',  'sex': 'H',  'edad':42},
                {'id': '3',  'sex': 'M',  'edad':29},
                {'id': '4',  'sex': 'M',  'edad':26},
                {'id': '5',  'sex': 'H',  'edad':21},
                {'id': '6',  'sex': 'M',  'edad':22},
                {'id': '7',  'sex': 'H',  'edad':23},
                {'id': '8',  'sex': 'H',  'edad':42},
                {'id': '9',  'sex': 'M',  'edad':29},
                {'id': '10', 'sex': 'M',  'edad':26},
                {'id': '11', 'sex': 'H',  'edad':21},
                {'id': '12', 'sex': 'M',  'edad':22},
                {'id': '13', 'sex': 'H',  'edad':23},
                {'id': '14', 'sex': 'H',  'edad':42},
                {'id': '15', 'sex': 'M',  'edad':29},
                {'id': '16', 'sex': 'M',  'edad':26},
                ]
        }

        expected_result1 = [
            {'option': 'Option 2', 'number': 2, 'votes': 750000, 'escanio': 6, 'paridad':[{'id': '3', 'sex': 'M', 'edad': 29}, 
                                                                                        {'id': '1', 'sex': 'H', 'edad': 23}, 
                                                                                        {'id': '4', 'sex': 'M', 'edad': 26}, 
                                                                                        {'id': '2', 'sex': 'H', 'edad': 42}, 
                                                                                        {'id': '6', 'sex': 'M', 'edad': 22}, 
                                                                                        {'id': '5', 'sex': 'H', 'edad': 21}]},
            {'option': 'Option 3', 'number': 3, 'votes': 500000, 'escanio': 4, 'paridad': [{'id': '3', 'sex': 'M', 'edad': 29}, 
                                                                                        {'id': '1', 'sex': 'H', 'edad': 23}, 
                                                                                        {'id': '4', 'sex': 'M', 'edad': 26}, 
                                                                                        {'id': '2', 'sex': 'H', 'edad': 42},
                                                                                        ]},
            {'option': 'Option 1', 'number': 1, 'votes': 300000, 'escanio': 2, 'paridad' : [
                                                                                            {'id': '3', 'sex': 'M', 'edad': 29}, 
                                                                                            {'id': '1', 'sex': 'H', 'edad': 23},
                                                                                            ]},
            {'option': 'Option 4', 'number': 4, 'votes': 250000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
            {'option': 'Option 5', 'number': 5, 'votes': 250000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
            {'option': 'Option 6', 'number': 6, 'votes': 250000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result1)
    
    def test_dhondtParidad2(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 300000},
                {'option': 'Option 2', 'number': 2, 'votes': 750000},
                {'option': 'Option 3', 'number': 3, 'votes': 500000},
                {'option': 'Option 4', 'number': 4, 'votes': 250000},
                {'option': 'Option 5', 'number': 5, 'votes': 250000},
                {'option': 'Option 6', 'number': 6, 'votes': 250000},
                  
            ],
            'escanio': 10,
            'candidates': [
                {'id': '1',  'sex': 'H',  'edad':23},
                {'id': '2',  'sex': 'H',  'edad':42},
                {'id': '3',  'sex': 'M',  'edad':29},
                {'id': '4',  'sex': 'M',  'edad':26},
                {'id': '10', 'sex': 'M',  'edad':26},
                {'id': '11', 'sex': 'H',  'edad':21},
                {'id': '12', 'sex': 'M',  'edad':22},
                {'id': '13', 'sex': 'H',  'edad':23},
                {'id': '14', 'sex': 'H',  'edad':42},
                {'id': '15', 'sex': 'M',  'edad':29},
                {'id': '16', 'sex': 'M',  'edad':26},
                ]
        }

        expected_result1 = [
            {'option': 'Option 2', 'number': 2, 'votes': 750000, 'escanio': 4, 'paridad':[{'id': '3', 'sex': 'M', 'edad': 29}, 
                                                                                        {'id': '1', 'sex': 'H', 'edad': 23}, 
                                                                                        {'id': '4', 'sex': 'M', 'edad': 26}, 
                                                                                        {'id': '2', 'sex': 'H', 'edad': 42}
                                                                                        ]
            },
            {'option': 'Option 3', 'number': 3, 'votes': 500000, 'escanio': 2, 'paridad': [{'id': '3', 'sex': 'M', 'edad': 29}, 
                                                                                        {'id': '1', 'sex': 'H', 'edad': 23},
                                                                                        ]},
            {'option': 'Option 1', 'number': 1, 'votes': 300000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
            {'option': 'Option 4', 'number': 4, 'votes': 250000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
            {'option': 'Option 5', 'number': 5, 'votes': 250000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
            {'option': 'Option 6', 'number': 6, 'votes': 250000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result1)
    # Test con valores correctos
    def test_dhondt2(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 510},
                {'option': 'Option 2', 'number': 2, 'votes': 250},
                {'option': 'Option 3', 'number': 3, 'votes': 450},
                {'option': 'Option 4', 'number': 4, 'votes': 300},
                {'option': 'Option 5', 'number': 5, 'votes': 150},
            ],
            'escanio': 7,
            'candidates': []
        }

        expected_result2 = [
            {'option': 'Option 1', 'number': 1, 'votes': 510, 'escanio': 3},
            {'option': 'Option 3', 'number': 3, 'votes': 450, 'escanio': 2},
            {'option': 'Option 2', 'number': 2, 'votes': 250, 'escanio': 1}, 
            {'option': 'Option 4', 'number': 4, 'votes': 300, 'escanio': 1},
            {'option': 'Option 5', 'number': 5, 'votes': 150, 'escanio': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result2)

    # Test con valores correctos
    def test_dhondt3(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 32},
                {'option': 'Option 2', 'number': 2, 'votes': 20},
                {'option': 'Option 3', 'number': 3, 'votes': 58},
            ],
            'escanio': 5,
            'candidates': []
        }

        expected_result3 = [
            {'option': 'Option 3', 'number': 3, 'votes': 58, 'escanio': 3},
            {'option': 'Option 1', 'number': 1, 'votes': 32, 'escanio': 1},
            {'option': 'Option 2', 'number': 2, 'votes': 20, 'escanio': 1},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result3)

    # Test con valores esperados erróneos
    def test_dhondt4(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 60},
                {'option': 'Option 2', 'number': 2, 'votes': 36},
                {'option': 'Option 3', 'number': 3, 'votes': 84},
            ],
            'escanio': 6,
            'candidates': []
        }

        expected_result4 = [
            {'option': 'Option 3', 'number': 3, 'votes': 58, 'escanio': 3},
            {'option': 'Option 1', 'number': 1, 'votes': 32, 'escanio': 1},
            {'option': 'Option 2', 'number': 2, 'votes': 20, 'escanio': 1},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, expected_result4)


    # Test con valores esperados erróneos
    def test_dhondt5(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 432},
                {'option': 'Option 2', 'number': 2, 'votes': 943},
                {'option': 'Option 3', 'number': 3, 'votes': 645},
                {'option': 'Option 4', 'number': 4, 'votes': 213},
            ],
            'escanio': 10,
            'candidates': []
        }

        expected_result5 = [
            {'option': 'Option 3', 'number': 3, 'votes': 645, 'escanio': 2},
            {'option': 'Option 1', 'number': 1, 'votes': 432, 'escanio': 5},
            {'option': 'Option 2', 'number': 2, 'votes': 943, 'escanio': 3},
            {'option': 'Option 4', 'number': 4, 'votes': 213, 'escanio': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, expected_result5)

    # Test con valores esperados erróneos
    def test_dhondt6(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 42},
                {'option': 'Option 2', 'number': 2, 'votes': 83},
                {'option': 'Option 3', 'number': 3, 'votes': 76},
            ],
            'escanio': 2,
            'candidates': []
        }

        expected_result6 = [
            {'option': 'Option 2', 'number': 2, 'votes': 83, 'escanio': 2},
            {'option': 'Option 3', 'number': 3, 'votes': 32, 'escanio': 0},
            {'option': 'Option 1', 'number': 1, 'votes': 20, 'escanio': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, expected_result6)
    
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
        self.assertEqual(values,res)

        
    def test_saintelague1(self):
        datos = {
            'type': 'SAINTELAGUE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 340000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 280000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 160000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 60000 },
               
            ],
             'escanio': 7
        }

        resultado_esperado = [
            { 'option': 'Option 1', 'number': 1, 'votes': 340000, 'escanio': 3},
            { 'option': 'Option 2', 'number': 2, 'votes': 280000, 'escanio': 3 },
            { 'option': 'Option 3', 'number': 3, 'votes': 160000, 'escanio': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 60000, 'escanio': 0 },

           
        ]


        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado_esperado)
    
    def test_saintelague2(self):
        datos = {
            'type': 'SAINTELAGUE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 50 },
                { 'option': 'Option 2', 'number': 2, 'votes': 40 },
                { 'option': 'Option 3', 'number': 3, 'votes': 20 },
               
            ],
             'escanio': 4
        }

        resultado_esperado = [
            { 'option': 'Option 1', 'number': 1, 'votes': 50, 'escanio': 2},
            { 'option': 'Option 2', 'number': 2, 'votes': 40, 'escanio': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 20, 'escanio': 1 },

           
        ]


        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado_esperado)

    def test_saintelague3(self):
        datos = {
            'type': 'SAINTELAGUE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 50 },
                { 'option': 'Option 2', 'number': 2, 'votes': 40 },
                { 'option': 'Option 3', 'number': 3, 'votes': 20 },
               
            ],
             'escanio': 5
        }

        resultado_esperado = [
            { 'option': 'Option 1', 'number': 1, 'votes': 50, 'escanio': 2},
            { 'option': 'Option 2', 'number': 2, 'votes': 40, 'escanio': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 20, 'escanio': 1 },

           
        ]


        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado_esperado)
   
   
    def test_saintelague4(self):
        datos = {
            'type': 'SAINTELAGUE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 5 },
                { 'option': 'Option 3', 'number': 3, 'votes': 2 },
               
            ],
             'escanio': 2
        }

        resultado_esperado = [
            { 'option': 'Option 2', 'number': 2, 'votes': 5, 'escanio': 2},
            { 'option': 'Option 1', 'number': 1, 'votes': 0, 'escanio': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 2, 'escanio': 0 },

           
        ]


        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado_esperado)
    
    def test_saintelague5(self):
        datos = {
            'type': 'SAINTELAGUE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 5 },
                { 'option': 'Option 3', 'number': 3, 'votes': 2 },
               
            ],
             'escanio': 2
        }

        resultado_esperado = [
            { 'option': 'Option 2', 'number': 2, 'votes': 5, 'escanio': 2},
            { 'option': 'Option 1', 'number': 1, 'votes': 0, 'escanio': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 2, 'escanio': 0 },

           
        ]


        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, resultado_esperado)

    def test_saintelague6(self):
        data = {
            'type': 'SAINTELAGUETCP',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 100000},
                {'option': 'Option 2', 'number': 2, 'votes': 75000},
                {'option': 'Option 3', 'number': 3, 'votes': 50000},
                {'option': 'Option 4', 'number': 4, 'votes': 25000},
            ],
            'escanio': 5,
            'candidates': [
                {'id': '1', 'sex': 'H',  'edad':23},
                {'id': '2', 'sex': 'H',  'edad':42},
                {'id': '3', 'sex': 'M',  'edad':29},
                {'id': '4', 'sex': 'M',  'edad':26},
                {'id': '5', 'sex': 'H',  'edad':21},
                {'id': '6', 'sex': 'M',  'edad':22},]
        }

        resultado_esperado = [
            {'option': 'Option 1', 'number': 1, 'votes': 100000, 'escanio': 2, 'paridad':[
                                                        {'id': '3', 'sex': 'M', 'edad': 29}, 
                                                        {'id': '1', 'sex': 'H', 'edad': 23}]},
            {'option': 'Option 2', 'number': 2, 'votes': 75000, 'escanio': 2, 'paridad': [
                                                        {'id': '3', 'sex': 'M', 'edad': 29}, 
                                                        {'id': '1', 'sex': 'H', 'edad': 23}]},
            {'option': 'Option 3', 'number': 3, 'votes': 50000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
            {'option': 'Option 4', 'number': 4, 'votes': 25000, 'escanio': 0, 'paridad' : []},
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado_esperado)


    def test_saintelague7(self):
        data = {
            'type': 'SAINTELAGUETCP',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 100000},
                {'option': 'Option 2', 'number': 2, 'votes': 75000},
                {'option': 'Option 3', 'number': 3, 'votes': 50000},
                {'option': 'Option 4', 'number': 4, 'votes': 25000},
            ],
            'escanio': 5,
            'candidates': [
                {'id': '1', 'sex': 'H',  'edad':23},
                {'id': '2', 'sex': 'H',  'edad':42},
                {'id': '3', 'sex': 'M',  'edad':29},
                {'id': '4', 'sex': 'M',  'edad':26},
                {'id': '5', 'sex': 'H',  'edad':21},
                {'id': '6', 'sex': 'M',  'edad':22},]
        }

        resultado_esperado = [
            {'option': 'Option 1', 'number': 1, 'votes': 100000, 'escanio': 2, 'paridad':[
                                                        {'id': '3', 'sex': 'M', 'edad': 29}, 
                                                        {'id': '1', 'sex': 'H', 'edad': 23}]},
            {'option': 'Option 2', 'number': 2, 'votes': 75000, 'escanio': 2, 'paridad': [
                                                        {'id': '3', 'sex': 'M', 'edad': 29}, 
                                                        {'id': '1', 'sex': 'H', 'edad': 23}]},
            {'option': 'Option 3', 'number': 3, 'votes': 50000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 29}]},
            {'option': 'Option 4', 'number': 4, 'votes': 25000, 'escanio': 0, 'paridad' : [{'id': '1', 'sex': 'H', 'edad': 23}]},
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, resultado_esperado)


    
    def test_saintelague8(self):
        data = {
            'type': 'SAINTELAGUETCP',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 100000},
                {'option': 'Option 2', 'number': 2, 'votes': 75000},
                {'option': 'Option 3', 'number': 3, 'votes': 50000},
            ],
            'escanio': 5,
            'candidates': [
                {'id': '1', 'sex': 'H',  'edad':41},
                {'id': '3', 'sex': 'M',  'edad':32},
                {'id': '4', 'sex': 'M',  'edad':19},
                {'id': '5', 'sex': 'H',  'edad':37},]
        }

        resultado_esperado = [
            {'option': 'Option 1', 'number': 1, 'votes': 100000, 'escanio': 2, 'paridad':[
                                                        {'id': '3', 'sex': 'M', 'edad': 32}, 
                                                        {'id': '1', 'sex': 'H', 'edad': 41}]},
            {'option': 'Option 2', 'number': 2, 'votes': 75000, 'escanio': 2, 'paridad': [
                                                        {'id': '3', 'sex': 'M', 'edad': 32}, 
                                                        {'id': '1', 'sex': 'H', 'edad': 41}]},
            {'option': 'Option 3', 'number': 3, 'votes': 50000, 'escanio': 1, 'paridad' : [{'id': '3', 'sex': 'M', 'edad': 32}]},
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado_esperado)

    

