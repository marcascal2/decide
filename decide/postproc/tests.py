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

    #Test con valores correctos
    def test_dhondt1(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 100000},
                {'option': 'Option 2', 'number': 2, 'votes': 75000},
                {'option': 'Option 3', 'number': 3, 'votes': 50000},
                {'option': 'Option 4', 'number': 4, 'votes': 25000},
            ],
            'nSeats': 5
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 100000, 'seat': 2},
            {'option': 'Option 2', 'number': 2, 'votes': 75000, 'seat': 2},
            {'option': 'Option 3', 'number': 3, 'votes': 50000, 'seat': 1},
            {'option': 'Option 4', 'number': 4, 'votes': 25000, 'seat': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Test con valores correctos
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
            'nSeats': 7
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 510, 'seat': 3},
            {'option': 'Option 3', 'number': 3, 'votes': 450, 'seat': 2},
            {'option': 'Option 2', 'number': 2, 'votes': 250, 'seat': 1}, 
            {'option': 'Option 4', 'number': 4, 'votes': 300, 'seat': 1},
            {'option': 'Option 5', 'number': 5, 'votes': 150, 'seat': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Test con valores correctos
    def test_dhondt3(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 32},
                {'option': 'Option 2', 'number': 2, 'votes': 20},
                {'option': 'Option 3', 'number': 3, 'votes': 58},
            ],
            'nSeats': 5
        }

        expected_result = [
            {'option': 'Option 3', 'number': 3, 'votes': 58, 'seat': 3},
            {'option': 'Option 1', 'number': 1, 'votes': 32, 'seat': 1},
            {'option': 'Option 2', 'number': 2, 'votes': 20, 'seat': 1},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    # Test con valores esperados erróneos
    def test_dhondt4(self):
        data = {
            'type': 'DHONDT',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 60},
                {'option': 'Option 2', 'number': 2, 'votes': 36},
                {'option': 'Option 3', 'number': 3, 'votes': 84},
            ],
            'nSeats': 6
        }

        expected_result = [
            {'option': 'Option 3', 'number': 3, 'votes': 58, 'seat': 3},
            {'option': 'Option 1', 'number': 1, 'votes': 32, 'seat': 1},
            {'option': 'Option 2', 'number': 2, 'votes': 20, 'seat': 1},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, expected_result)

    