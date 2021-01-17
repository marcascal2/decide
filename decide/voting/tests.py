import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from pathlib import Path
from django.urls import reverse
import os
from datetime import datetime

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption, QuestionPrefer, QuestionOrdering, Candidate, ReadonlyVoting, MultipleVoting, Party, Program, Plank
from django.test import TestCase, override_settings
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')

class VotingToString(BaseTestCase):

    def setUp(self):
        q=Question(desc="Descripcion")
        q.save()

        que1=Question(desc="Descripcion1")
        que1.save()
        que2=Question(desc="Descripcion2")
        que2.save()

        opt1 = QuestionOption(question = q, option = "option1")
        opt1.save()

        opt2 = QuestionOption(question = q, option = "option2")
        opt2.save()

        q_prefer = QuestionPrefer(question = q, prefer = "YES", number = 4, option="option1")
        q_prefer.save()

        q_ordering = QuestionOrdering(question=q, number = 5, option="prueba de ordenacion", ordering=1)
        q_ordering.save()

        party1 = Party(abreviatura = "PC")
        party1.save()

        self.candidate1 = Candidate(name="test", age=21, number=1, auto_community="AN", sex ="H", political_party = party1)
        self.candidate1.save()

        self.v1 = ReadonlyVoting(name="VotacionRO", question=que1, desc = "example")
        self.v2 = MultipleVoting(name="VotacionM", desc = "example")
        self.v2.save()
        self.v2.question.add(que1)
        self.v2.question.add(que2)
        self.v=Voting(name="Votacion", question=q)
        self.v.save()
        self.v1.save()
        self.v2.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v = None

    def test_Voting_toString(self):
        v = Voting.objects.get(name = 'Votacion')
        v1 = ReadonlyVoting.objects.get(name = 'VotacionRO')
        v2 = MultipleVoting.objects.get(name = 'VotacionM')
        candidate1 = Candidate.objects.get(name = 'test')
        self.assertEquals(str(v),"Votacion")
        self.assertEquals(str(v.question),"Descripcion")
        self.assertEquals(str(v.question.options.all()[0]),"option1 (2)")
        self.assertEquals(str(v.question.prefer_options.all()[0]), "option1 (4)")
        self.assertEquals(str(v.question.options_ordering.all()[0]), "prueba de ordenacion (5)")
        self.assertEquals(str(candidate1), "test (21) - AN - H - PC")
        self.assertEquals(str(v1),"VotacionRO")
        self.assertEquals(str(v2),"VotacionM")

class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q, escanios =20)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v


    def create_voting_prefer(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionPrefer(question=q, prefer = 'YES',option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
        
    def create_voting_custom_url(self):
        q = Question(desc='new test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='new test voting', question=q, customURL='custom')
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'escanios': 20,
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_create_voting_with_end_date_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'escanios': 20,
            'question_opt': ['cat', 'dog', 'horse'],
            'end_date': '2024-12-21T11:33:23Z'
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201) 

    def test_create_voting_with_start_date_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'escanios': 10,
            'question_opt': ['cat', 'dog', 'horse'],
            'start_date': '2021-10-18T10:28:19Z'
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201) 

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')
        
        #Comprobar que se ha creado el archivo
        self.test_createfiles_voting()

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')

    def test_complete_voting_prefer(self):
        v = self.create_voting_prefer()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])


    def test_create_voting_prefer_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'escanios': 20,
            'question_opt' : [],
            'question_pref': ['CAT', 'DOG', 'HORSE']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def testVotingCandidateFromApi(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'escanios': 20,
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse'],
            'candidates' :
            {
                'name': 'pepe',
                'sex': 'H',
                'auto_community': 'H',
                'age': 21,
                'political_party': 
                {   
                    'abreviatura': 'PC',
                    'nombre': 'Partido Cuestista',
                    'program':
                    {
                        'title': 'programa de PC',
                        'overview': 'el programa politico del PC',
                        'plank': ['promesa1', 'promesa2', 'promesa3'],

                    }
                }
                
            }
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)


    def testVotingWithManyCandidateFromApi(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'escanios': 20,
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse'],
            'candidates' :
            [{
                'name': 'pepe',
                'sex': 'H',
                'auto_community': 'H',
                'age': 21,
                'political_party': 
                {   
                    'abreviatura': 'PACMA',
                    'nombre': 'Partido Animalista'
                }
            },
            {
                'name': 'pepe2',
                'sex': 'H',
                'auto_community': 'BA',
                'age': 21,
                'political_party': 
                {   
                    'abreviatura': 'VOX',
                    'nombre': 'VOX'
                }  
            },           
            { 
                'name': 'pepe3',
                'sex': 'M',
                'auto_community': 'AN',
                'age': 30,
                'political_party': 
                {   
                    'abreviatura': 'UP',
                    'nombre': 'Unidas Podemos'
                } 
            }
            ]
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    # def test_complete_voting_custom(self):
    #     v = self.create_voting_custom_url()
    #     self.create_voters(v)

    #     v.create_pubkey()
    #     v.start_date = timezone.now()
    #     v.save()

    #     response = self.client.head(reverse('customURL',args=['custom']))
    #     self.assertEqual(response.status_code, 200)
        
    def test_createfiles_voting(self):
        _datetime = datetime.now()
        datetime_str = _datetime.strftime("%Y-%m-%d-%H")
        path = 'archivosGuardados/'+datetime_str+'.zip'
        self.assertTrue(os.path.exists(path))

class QuestionTestCase(BaseTestCase):

    def setUp(self):
        q=Question(desc="Descripcion")
        q.save()

        self.v=Voting(name="Votacion", question=q)
        self.v.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v=None

    def testExistQuestionNoOption(self):
        v = Voting.objects.get(name="Votacion")
        self.assertEqual(v.question.desc, "Descripcion")
    def testExistQuestionWithOption(self):
        q = Question.objects.get(desc="Descripcion")
        opt1 = QuestionOption(question = q, option="option1")
        opt1.save()
        v = Voting.objects.get(name="Votacion")
        v.question = q
        v.question_opt = opt1
        v.save()
        self.assertEqual(v.question.options.all()[0].option, "option1")
    def testExistQuestionWithPrefer(self):
        q = Question.objects.get(desc="Descripcion")
        opt1 = QuestionPrefer(question = q, prefer = "YES" ,option="option1")
        opt1.save()
        v = Voting.objects.get(name="Votacion")
        v.question = q
        v.question_pref = opt1
        v.save()
        self.assertEqual(v.question.prefer_options.all()[0].option, "option1")
        self.assertEqual(v.question.prefer_options.all()[0].prefer, "YES")
    def testAddOption(self):
        v = Voting.objects.get(name="Votacion")
        q = v.question

        self.assertEqual(v.question.options.all().count(),0)

        opt = QuestionOption(question=q, option="opcionTest")
        opt.save()
        v.save()

        self.assertEqual(v.question.options.all()[0].option , "opcionTest")
        self.assertEqual(v.question.options.all().count(),1)

    def testAddOptionPrefer(self):
        v = Voting.objects.get(name="Votacion")
        q = v.question

        self.assertEqual(v.question.prefer_options.all().count(),0)

        opt = QuestionPrefer(question=q, prefer = 'YES', option="opcionTest")
        opt.save()
        v.save()

        self.assertEqual(v.question.prefer_options.all()[0].option , "opcionTest")
        self.assertEqual(v.question.prefer_options.all()[0].prefer, "YES")
        self.assertEqual(v.question.prefer_options.all().count(),1)

class AgeTestCase(BaseTestCase):

    def setUp(self):
        q=Question(desc="Descripcion")
        q.save()

        opt1 = QuestionOption(question = q, option = "option1")
        opt1.save()

        opt2 = QuestionOption(question = q, option = "option2")
        opt2.save()

        self.v=Voting(name="Votacion", question=q)
        self.v.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v = None

    def create_wrong_voting(self):
        
        q = Question(desc='test question')

        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q, min_age = "0", max_age = "354")
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    

    def testExistWithoutAges(self):
        v = Voting.objects.get(name="Votacion")
        self.assertEquals(v.question.desc, "Descripcion")
        self.assertEquals(v.question.options.all()[0].option, "option1")
        self.assertEquals(v.question.options.all()[1].option, "option2")
    
    def testExistWithMinAge(self):
        v = Voting.objects.get(name = "Votacion")
        v.min_age = 4
        self.assertEquals(v.min_age, 4)
    
    def testExistWithMaxAge(self):
        v = Voting.objects.get(name = "Votacion")
        v.max_age = 30
        self.assertEquals(v.max_age, 30)

    def testExistWithBoth(self):
        v = Voting.objects.get(name = "Votacion")
        v.min_age = 5
        v.max_age = 82
        self.assertEquals(v.min_age, 5)
        self.assertEquals(v.max_age, 82)

    def testSaveMinAge(self):
        v = Voting.objects.get(name = "Votacion")
        self.assertEquals(v.min_age, None)

        v.min_age = 2
        v.save()

        self.assertEquals(v.min_age, 2)
    
    def testSaveMaxAge(self):
        v = Voting.objects.get(name = "Votacion")
        self.assertEquals(v.max_age, None)

        v.max_age = 23
        v.save()

        self.assertEquals(v.max_age, 23)

class VotingOrderingTestCase(BaseTestCase):

    def create_ordering_voting(self):
        q = Question(desc='Testeo de una order_ question')
        q.save()
        for i in range(5):
            opt = QuestionOrdering(question=q, option='ordering {}'.format(i+1), ordering='{}'.format(i+1))
            opt.save()
        v = Voting(name='Testeo de una order_ voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    def test_create_ordering_voting_from_api(self):
        data = {'name': 'Example'}

        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'escanios': 20,
            'question_opt': [],
            'question_ordering': [2,1,3]
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

class QuestionOrderingTestCase(BaseTestCase):

    def setUp(self):
        q=Question(desc="Descripcion")
        q.save()

        self.v=Voting(name="Votacion", question=q)
        self.v.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v=None
 
    def testExistQuestionNoOption(self):
        v = Voting.objects.get(name="Votacion")
        self.assertEquals(v.question.desc, "Descripcion")
    
    def testExistQuestionWithOption(self):
        q = Question.objects.get(desc="Descripcion")
        opt1 = QuestionOption(question = q, option="option1")
        opt1.save()
        v = Voting.objects.get(name="Votacion")
        v.question = q
        v.question_opt = opt1
        v.save()
        self.assertEquals(v.question.options.all()[0].option, "option1")

    def testExistQuestionWithOrdering(self):
        q = Question.objects.get(desc="Descripcion")
        q.save()

        q_order1 = QuestionOrdering(question=q,option="esta va a salir segunda",ordering=1)
        q_order1.save()
        q_order2 = QuestionOrdering(question=q,option="esta va a salir primera" ,ordering=2)
        q_order2.save()

        v= Voting(name="Prueba votacion ordenada", question=q)
        v.save()

        q_order1_postgres=Voting.objects.get(name="Prueba votacion ordenada").question.options_ordering.filter(option="esta va a salir segunda").get()
        q_order2_postgres=Voting.objects.get(name="Prueba votacion ordenada").question.options_ordering.filter(option="esta va a salir primera").get()

        self.assertEquals(q_order1_postgres.ordering, 1)
        self.assertEquals(q_order2_postgres.ordering, 2)


    def testExistQuestionWithFailureOrdering(self):
        q = Question.objects.get(desc="Descripcion")
        q.save()

        q_order1 = QuestionOrdering(question=q,option="esta va a salir segunda",ordering=1)
        q_order1.save()
        q_order2 = QuestionOrdering(question=q,option="esta va a salir primera" ,ordering=2)
        q_order2.save()

        v= Voting(name="Prueba votacion ordenada", question=q)
        v.save()

        q_order1_postgres=Voting.objects.get(name="Prueba votacion ordenada").question.options_ordering.filter(option="esta va a salir segunda").get()
        q_order2_postgres=Voting.objects.get(name="Prueba votacion ordenada").question.options_ordering.filter(option="esta va a salir primera").get()

        self.assertNotEquals(q_order1_postgres.ordering, 2)
        self.assertNotEquals(q_order2_postgres.ordering, 1)

class CandidateTestCase(BaseTestCase):

    def setUp(self):
        p = Party(abreviatura = "PC")
        p.save()
        c = Candidate(name="pepe")
        c.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v=None 


    def testExistCandidate(self):
        candidate_test= Candidate.objects.get(name="pepe")
        self.assertEqual(candidate_test.name, "pepe")

    def testExistCompleteCandidate(self):
        p1 = Party(abreviatura = "PC")
        candidate_test = Candidate(name="test", age=21, number=1, auto_community="AN", sex ="H", political_party = p1)
        self.assertEqual(candidate_test.name, "test")
        self.assertEqual(candidate_test.age, 21)
        self.assertEqual(candidate_test.number, 1)
        self.assertEqual(candidate_test.auto_community, "AN")
        self.assertEqual(candidate_test.sex, "H")
        self.assertEqual(candidate_test.political_party.abreviatura, "PC")


class PartyTestCase(BaseTestCase):

    def setUp(self):
        self.p = self.create_party()
        self.p.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def create_party(self):
        p = Program(title='programa test')
        p.save()
        for i in range(5):
            plk = Plank(program=p, plank='plank {}'.format(i+1))
            plk.save()
        pt = Party(abreviatura = 'PC', nombre='Partido Cuestista', program=p)
        pt.save()

        return pt    

    def testExistParty(self):
        p = Party.objects.get(abreviatura = "PC")
        self.assertEquals(p.abreviatura, "PC")

    def testExistCompleteParty(self):
        p = Party.objects.get(abreviatura = "PC")
        self.assertEquals(p.abreviatura, "PC")
        self.assertEquals(p.nombre , "Partido Cuestista")
        self.assertEquals(p.program.title , "programa test")
        #for plk in p.program.planks.all():
    

    def testUpdateCompleteParty(self):
        p = Party.objects.get(abreviatura = "PC")
        p.abreviatura = "PG"
        p.nombre = "Partido Guerrista"
        self.assertEquals(p.abreviatura, "PG")
        self.assertEquals(p.nombre, "Partido Guerrista")


class ProgramTestCase(BaseTestCase):

    def setUp(self):
        p=Program(title="test de Programa")
        p.save()

        self.pt=Party(abreviatura="TP", nombre='test party', program=p)
        self.pt.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.pt=None

    def testExistProgramNoPlank(self):
        pt = Party.objects.get(abreviatura="TP")
        self.assertEqual(pt.program.title, "test de Programa")

    def testExistProgramWithPlank(self):
        p = Program.objects.get(title="test de Programa")
        plk1 = Plank(program = p, plank="plank1")
        plk1.save()
        pt = Party.objects.get(abreviatura="TP")
        pt.program = p
        pt.plank = plk1
        pt.save()
        self.assertEqual(pt.program.planks.all()[0].plank, "plank1")
    
    def testAddPlank(self):
        pt = Party.objects.get(abreviatura="TP")
        p = pt.program

        self.assertEqual(pt.program.planks.all().count(),0)

        plk = Plank(program = p, plank="plank")
        plk.save()
        pt.save()

        self.assertEqual(pt.program.planks.all()[0].plank , "plank")
        self.assertEqual(pt.program.planks.all().count(),1)



class ReadOnlyVotingTests(BaseTestCase):

    def setUp(self):
        q=Question(desc="Descripcion")
        q.save()

        opt1 = QuestionOption(question = q, option = "option1")
        opt1.save()

        opt2 = QuestionOption(question = q, option = "option2")
        opt2.save()

        self.v=ReadonlyVoting(name="Votacion", question=q, desc = "example")
        self.v.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v = None

    def testExistReadonlyVoting(self):
        v = ReadonlyVoting.objects.get(name="Votacion")
        self.assertEquals(v.question.desc, "Descripcion")
        self.assertEquals(v.desc, "example")
        self.assertEquals(v.question.options.all()[0].option, "option1")
        self.assertEquals(v.question.options.all()[1].option, "option2")

    def testUpdateReadonlyVotingDesc(self):
        v = ReadonlyVoting.objects.get(name="Votacion")
        v.desc = "cambio"
        self.assertEquals(v.desc, "cambio")
        # Mediante tests las Readonly Voting si se pueden cambiar pese a que en la página no puedan hacerlo los usuarios
        
    def testDeleteReadonlyVotingDesc(self):
        v = ReadonlyVoting.objects.get(name="Votacion")
        v.desc = None
        self.assertEquals(v.desc, None)

    def testDeleteReadonlyVoting(self):
        v = ReadonlyVoting.objects.get(name="Votacion")
        v2 = ReadonlyVoting.objects.get(name="Votacion")
        v.delete()
        self.assertNotEquals(v, v2)

    def test_update_voting(self):
        # No se pueden votar este tipo porque habria que tocar la cabina de votaciones y el visualizer, asi que comprobamos que efectivamente no se puede votar

        voting = ReadonlyVoting.objects.get(name="Votacion")

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # STATUS VOTING: not started
        for action in ['stop']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 403)

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

class MultipleVotingTests(BaseTestCase):

    def setUp(self):
        q = Question(desc='multiple test question')
        q2 = Question(desc='multiple test question 2')
        q3 = Question(desc='multiple test question 3')
        q.save()
        q2.save()
        q3.save()
        for i in range(3):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        for i in range(4):
            opt = QuestionOption(question=q2, option='option {}'.format(i+1))
            opt.save()
        for i in range(5):
            opt = QuestionOption(question=q3, option='option {}'.format(i+1))
            opt.save()
    
        self.v=MultipleVoting(name="Votacion", desc = "example")
        self.v.save()
        self.v.question.add(q)
        self.v.question.add(q2)
        self.v.save()

        self.v=MultipleVoting(name="Votacion2", desc = "example2")
        self.v.save()
        self.v.question.add(q)
        self.v.save()

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v = None

    def testCreateMultipleVotingWithTwoQuestions(self):
        v = MultipleVoting.objects.get(name="Votacion")
        self.assertEquals(v.desc, "example")
        self.assertEquals(v.question.all()[0].desc, "multiple test question")
        self.assertEquals(v.question.all()[1].desc, "multiple test question 2")

    def testCreateMultipleVotingWithOneQuestion(self):
        v = MultipleVoting.objects.get(name="Votacion2")
        self.assertEquals(v.desc, "example2")
        self.assertEquals(v.question.all()[0].desc, "multiple test question")
        with self.assertRaises(IndexError): v.question.all()[1].desc

    def testUpdateMultipleVotingWithTwoQuestions(self):
        v = MultipleVoting.objects.get(name="Votacion")
        v.desc = "cambio"
        v.question.add(Question.objects.get(desc="multiple test question 3"))
        self.assertEquals(v.desc, "cambio")
        self.assertEquals(v.question.all()[0].desc, "multiple test question")
        self.assertEquals(v.question.all()[1].desc, "multiple test question 2")
        self.assertEquals(v.question.all()[2].desc, "multiple test question 3")

    def testUpdateMultipleVotingWithOneQuestion(self):
        v = MultipleVoting.objects.get(name="Votacion2")
        v.desc = "cambio"
        v.question.add(Question.objects.get(desc="multiple test question 2"))
        self.assertEquals(v.desc, "cambio")
        self.assertEquals(v.question.all()[0].desc, "multiple test question")
        self.assertEquals(v.question.all()[1].desc, "multiple test question 2")

    def testUpdateMultipleVotingRemoveQuestion(self):
        v = MultipleVoting.objects.get(name="Votacion2")
        v.question.remove(Question.objects.get(desc="multiple test question 2"))
        self.assertEquals(v.desc, "example2")
        self.assertEquals(v.question.all()[0].desc, "multiple test question")
        with self.assertRaises(IndexError): v.question.all()[1].desc

    def testDeleteMultipleVoting(self):
        v = MultipleVoting.objects.get(name="Votacion")
        v2 = MultipleVoting.objects.get(name="Votacion")
        v.delete()
        self.assertNotEquals(v, v2)

    def test_update_voting(self):
        # No se pueden votar este tipo porque habria que tocar la cabina de votaciones y el visualizer, asi que comprobamos que efectivamente no se puede votar

        voting = MultipleVoting.objects.get(name="Votacion")

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # STATUS VOTING: not started
        for action in ['stop']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 403)

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

