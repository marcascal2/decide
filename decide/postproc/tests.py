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