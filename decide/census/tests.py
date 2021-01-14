import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Census
<<<<<<< HEAD
from census import views, admin
from voting.models import Voting, Question
=======
from census import views
from voting.models import Voting, Question, Candidate
>>>>>>> task/visualizacion-maria
from base import mods
from base.tests import BaseTestCase
from datetime import date
from django.test import RequestFactory, TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import io
import csv

class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.question = Question(desc='desc')
        self.question.save()

        v1 = Voting(id = 1, name='voting_testing1', question=self.question, escanios=30)
        v1.save()
        
        v2 = Voting(id = 3, name='voting_testing2', question=self.question, escanios=10)
        v2.save()

        user1 = User(id=5, username='voter1', password='test_password')
        user1.save()
        
        user2 = User(id=6, username='voter2', password='test_password')
        user2.save()

        self.census = Census(id=21, voting_id=1, voter_id=5, adscripcion='Colegio1', date=date.today())
        self.census.save()

        c2 = Census(id=22,voting_id=3, voter_id=5, adscripcion='Colegio1', date=date.today())
        c2.save()

        c3 = Census(id=23, voting_id=1, voter_id=6, adscripcion='Colegio2', date=date.today())
        c3.save()

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
        self.assertEqual(response.json(), {'voters': [5, 6]})

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

        self.login(user='admin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), 4)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, len(Census.objects.filter(voter_id=1)))

    def test_model(self):
        c = Census.objects.get(adscripcion = 'Colegio2')
        c.date = date.today
        self.assertEqual(c.voting_id, 1)
        self.assertEqual(c.voter_id, 6)
        self.assertEqual(c.adscripcion, 'Colegio2')
        self.assertEqual(c.date, date.today)
    
    def test_model_functions(self):
        c = self.census
        self.assertEqual(c.voting_name, 'voting_testing1')
        self.assertEqual(c.voting_question, 'desc')
        self.assertEqual(c.voter_username, 'voter1')
    
    def test_all_census(self):
        u = User(username='request_user', password='request_password')
        u.save()
        census = Census.objects.all()
        
        rf = RequestFactory()
        request = rf.get('/census/all_census/')  
        request.user = u
        response = views.all_census(request)
        
        for c in census:
            self.assertContains(response, c)

    def test_group_by_adscripcion(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=22)
        rf = RequestFactory()
        request = rf.get('/census/group_by_adscripcion/')  
        request.user = u
        response = views.group_by_adscripcion(request,'Colegio1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)

    def test_group_by_voting(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=23)
        rf = RequestFactory()
        request = rf.get('/census/group_by_voting/')  
        request.user = u
        response = views.group_by_voting(request,1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)

    def test_group_by_voter(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=22)
        rf = RequestFactory()
        request = rf.get('/census/group_by_voter/')  
        request.user = u
        response = views.group_by_voter(request,5)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)

    def test_group_by_date(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=22)
        c3 = Census.objects.get(id=23)
        rf = RequestFactory()
        request = rf.get('/census/group_by_date/')  
        request.user = u
        response = views.group_by_date(request,str(date.today()))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)
        self.assertContains(response, c3)

    def test_group_by_question(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=22)
        c3 = Census.objects.get(id=23)
        rf = RequestFactory()
        request = rf.get('/census/group_by_question/')  
        request.user = u
        response = views.group_by_question(request,'desc')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)
        self.assertContains(response, c3)

<<<<<<< HEAD
    def test_export_census_user(self):
        rf = RequestFactory()
        request = rf.get('/census/export_by_voting/{}'.format(1))  
        response = views.export_by_voting(request, '1')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        csv_reader = csv.reader(io.StringIO(content))
        num_row = sum(1 for row in csv_reader)
        #headers + 2 censos con voting_id == 1
        self.assertEqual(num_row, 3)

        csv_reader = csv.reader(io.StringIO(content))
        headers = next(csv_reader)
        self.assertIn('voter_id', headers)
        self.assertIn('adscripcion', headers)
        self.assertIn('date', headers)

    def test_export_census_user_void(self):
        rf = RequestFactory()
        request = rf.get('/census/export_by_voting/{}'.format(2))  
        response = views.export_by_voting(request, '2')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        csv_reader = csv.reader(io.StringIO(content))
        num_row = sum(1 for row in csv_reader)
        #solo hay headers ya que no existe el voting con id 2
        self.assertEqual(num_row, 1)

        csv_reader = csv.reader(io.StringIO(content))
        headers = next(csv_reader)
        self.assertIn('voter_id', headers)
        self.assertIn('adscripcion', headers)
        self.assertIn('date', headers)

    def test_export_census_admin(self):
        census = Census.objects.all()

        rf = RequestFactory()
        request = rf.post('', {'action': 'export_as_csv'})
        response = admin.CensusAdmin.export_as_csv(self,request,census)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        csv_reader = csv.reader(io.StringIO(content))
        num_row = sum(1 for row in csv_reader)
        #headers + 3 censos
        self.assertEqual(num_row, 4)

        csv_reader = csv.reader(io.StringIO(content))
        headers = next(csv_reader)
        self.assertIn('voter_id', headers)
        self.assertIn('adscripcion', headers)
        self.assertIn('date', headers)

    def test_import_census_user_correct(self):
        csv = open("census/testing_files/csv_user.csv", 'rb')
        data = SimpleUploadedFile(content = csv.read(), name = csv.name, content_type='multipart/form-data')
        u = User(username='request_user', password='request_password')
        u.save()

        rf = RequestFactory()
        content_type = 'multipart/form-data'
        headers= {
            'HTTP_CONTENT_TYPE': content_type,
            'HTTP_CONTENT_DISPOSITION': 'attachment; filename=csv_user.csv'}
        
        request = rf.post('upload.html', {'file': data}, **headers)
        request.user = u
        response = views.import_by_voting(request)

        self.assertEqual(response.status_code, 200)
        for row1, row2  in zip(request.FILES['file'], data):
            cadena1 = row1.decode('utf-8')
            cadena2 = row2.decode('utf-8')
            self.assertEqual(cadena1, cadena2)
        csv.close()

    def test_import_census_admin_correct(self):
        csv = open("census/testing_files/csv_admin.csv", 'rb')
        data = SimpleUploadedFile(content = csv.read(), name = csv.name, content_type='multipart/form-data')
        u = User(username='request_user', password='request_password')
        u.save()

        rf = RequestFactory()
        content_type = 'multipart/form-data'
        headers= {
            'HTTP_CONTENT_TYPE': content_type,
            'HTTP_CONTENT_DISPOSITION': 'attachment; filename=csv_admin.csv'}
        
        request = rf.post('upload.html', {'file': data}, **headers)
        request.user = u
        response = admin.CensusAdmin.import_from_csv(self, request)

        self.assertEqual(response.status_code, 200)
        for row1, row2  in zip(request.FILES['file'], data):
            cadena1 = row1.decode('utf-8')
            cadena2 = row2.decode('utf-8')
            self.assertEqual(cadena1, cadena2)
        csv.close()
        
=======
    def test_census_estatistics(self):
        census_per_voters = views.census_per_voters()
        self.assertEquals(census_per_voters['voter1'], 2)
        self.assertEquals(census_per_voters['voter2'], 1)
        escanios = views.escanios()
        self.assertEquals(escanios['voting_testing1'], 30)
        self.assertEquals(escanios['voting_testing2'], 10)
        voters = views.voters()
        self.assertEquals(voters['voting_testing1'], 2)
        self.assertEquals(voters['voting_testing2'], 1)
>>>>>>> task/visualizacion-maria
