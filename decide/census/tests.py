import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Census
from census import views
from voting.models import Voting, Question
from base import mods
from base.tests import BaseTestCase
from datetime import date
from django.test import RequestFactory, TestCase


class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.question = Question(desc='desc')
        self.question.save()
        self.voting = Voting(id = 1, name='voting_testing', question=self.question)
        self.voting.save()
        user1 = User(id=5, username='test', password='test_password')
        user1.save()
        self.census = Census(voting_id=1, voter_id=5)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_check_vote_permissions(self):
        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 5), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [5]})

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [5]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 2, 'voters': [1,2,3,4], 'adscripcion': 'Colegio 1'}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, len(Census.objects.filter(voter_id=1)))

    def test_model(self):
        self.census.adscripcion = 'ads'
        self.census.date = date.today
        self.assertEqual(self.census.voting_id, 1)
        self.assertEqual(self.census.voter_id, 5)
        self.assertEqual(self.census.adscripcion, 'ads')
        self.assertEqual(self.census.date, date.today)
    
    def test_model_functions(self):
        self.assertEqual(self.census.voting_name, 'voting_testing')
        self.assertEqual(self.census.voting_question, 'desc')
        self.assertEqual(self.census.voter_username, 'test')

    def test_group_by_voter(self):
        u = User(username='request_user', password='request_password')
        u.save()
        voter = User.objects.get(id = self.census.voter_id)
        voting = Voting.objects.get(id = self.census.voting_id)
        rf = RequestFactory()
        request = rf.get('/census/group_by_voter/')  
        request.user = u
        response = views.voter_census(request, 5)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, voter)
        self.assertContains(response, voting)
        # self.assertContains(response, self.census)
    
    def test_group_by_voting(self):
        u = User(username='request_user', password='request_password')
        u.save()
        voter = User.objects.get(id = self.census.voter_id)
        voting = Voting.objects.get(id = self.census.voting_id)
        rf = RequestFactory()
        request = rf.get('/census/group_by_voting/')  
        request.user = u
        response = views.voting_census(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, voter)
        self.assertContains(response, voting)
        # self.assertContains(response, self.census)