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



    def test_simple(self):
        data = {
            'type': 'SIMPLE',
            'seats': 7,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 }, 
                { 'option': 'Option 2', 'number': 2, 'votes': 2 },
                { 'option': 'Option 3', 'number': 3, 'votes': 5 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
        
            ]
        }

        expected_result = [
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
        self.assertEqual(values, expected_result)

    def test_simple1(self):
        data = {
            'type': 'SIMPLE',
            'seats':40,
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

    def test_simple2(self):
        data = {
            'type': 'SIMPLE',
            'seats':70,
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
            'seats':100,
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
            'seats':20,
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
            'seats':30,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 15 },
                { 'option': 'Option 2', 'number': 2, 'votes': 10 },
                { 'option': 'Option 3', 'number': 3, 'votes': 14},
                { 'option': 'Option 4', 'number': 4, 'votes': 5},
                { 'option': 'Option 5', 'number': 5, 'votes': 2 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
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