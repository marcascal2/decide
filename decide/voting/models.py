from django.db import models
from django.core.files import File
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.files.storage import default_storage
from datetime import datetime
import zipfile
import json
from base import mods
from base.models import Auth, Key

class Question(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc

class Program(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()

    def __str__(self):
        return self.title

class Party(models.Model):
    abreviatura = models.TextField(max_length=10)
    nombre = models.TextField()
    program = models.ForeignKey(Program, related_name='party', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.abreviatura        


class Plank(models.Model):
    program = models.ForeignKey(Program, related_name='planks', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    plank = models.TextField()

    def save(self):
        if not self.number:
            self.number = self.program.planks.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.plank, self.number)

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)

def validate_end_date(value):
    if value < timezone.now():
        raise ValidationError("La fecha de fin no puede anterior a este momento")
def validate_start_date(value):
    #end_date = 
    if value < timezone.now():
        raise ValidationError("La fecha introducida es inadecuada")
class QuestionPrefer(models.Model):
    question = models.ForeignKey(Question, related_name='prefer_options', on_delete=models.CASCADE)
    prefer = models.TextField(blank=True, choices=[('YES','YES')])
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self):
        if not self.number:
            self.number = self.question.prefer_options.count() + 2
        if not self.prefer:
            self.prefer = self.question.prefer_options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)
        
def validate_age(value):
    if value == 0 or value > 125:
        raise ValidationError("La edad debe ser mayor que 0 y menor que 125")


class QuestionOrdering(models.Model):
    question = models.ForeignKey(Question, related_name='options_ordering', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()
    ordering = models.PositiveIntegerField(blank=True, null=True)

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        if not self.ordering:
            self.ordering = self.question.options_ordering.count() + 2
        return super().save()
        

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)

class Candidate(models.Model):
    name = models.TextField()
    age = models.PositiveIntegerField(null=True)
    number = models.PositiveIntegerField(blank=True, null=True)

    PARTIDOS = (('PP', 'Partido popular'),
        ('PSOE', 'Partido Socialista Obrero Español'),
        ('UP', 'Unidas Podemos'),
        ('PACMA', 'PACMA'),
        ('VOX', 'VOX'),
        ('CS', 'Ciudadanos')    
    )
    COMUNIDADES = (('AN', 'Andalucia'),        
        ('AR', 'Aragon'),
        ('AS', 'Asturias'),    
        ('BA', 'Baleares'),     
        ('CA', 'Canarias'),
        ('CT', 'Cantabria'),         
        ('CAM', 'Castilla-Mancha'),  
        ('CAL', 'Castilla-Leon'),  
        ('CAT', 'Cataluña'),  
        ('CE', 'Ceuta'),  
        ('EX', 'Extremadura'),  
        ('GA', 'Galicia'),  
        ('LR', 'La-Rioja'),  
        ('MA', 'Madrid'), 
        ('ME', 'Melilla'),   
        ('MU', 'Murcia'),  
        ('NA', 'Navarra'),
        ('PV', 'País-Vasco'),
        ('VA', 'Valencia')) 
    auto_community = models.TextField(choices=COMUNIDADES, default='AN')
    sex = models.TextField(default='H', choices=[('H','HOMBRE'),('M','MUJER')])
    #political_party = models.TextField(choices= PARTIDOS, default = 'PACMA')
    political_party= models.ForeignKey(Party, related_name='candidate', on_delete=models.CASCADE,null=True)
    def __str__(self):
         return '{} ({}) - {} - {} - {}'.format(self.name, self.age, self.auto_community, self.sex, self.political_party)

class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE,null=True)
    candidates = models.ManyToManyField(Candidate, related_name='votings', blank = True)
    escanios = models.PositiveSmallIntegerField(default=0)
    location = models.TextField(blank=True, null=True)

    start_date = models.DateTimeField(blank=True, null=True, validators=[validate_start_date])
    end_date = models.DateTimeField(validators=[validate_end_date],blank=True, null=True)

    min_age = models.PositiveIntegerField(blank=True, null=True, validators=[validate_age])
    max_age = models.PositiveIntegerField(blank=True, null=True, validators=[validate_age])
    
    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')
    customURL = models.CharField(null=True, blank=True, unique=True, max_length=200)
    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def save(self):
        if self.start_date is not None and self.end_date is not None:
            if self.start_date > self.end_date :
                raise ValidationError("La fecha de inicio no puede ser anterior a la de fin")
        if self.min_age is not None and self.max_age is not None:
            if self.min_age > self.max_age :
                raise ValidationError("Edad máxima debe ser mayor que la edad mínima")
        return super().save()

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()
        #Aqui hacemos el guardado del Tally
        _datetime = datetime.now()
        datetime_str = _datetime.strftime("%Y-%m-%d-%H")
        with open ('archivosGuardados/tally','w') as f:
             for tallys in json.dumps(self.tally):
                 json.dump(tallys,f)
        self.do_postproc()
        #Aqui comprimo
        with zipfile.ZipFile('archivosGuardados/'+datetime_str+'.zip', 'w') as zf:
            zf.write('archivosGuardados/tally')
            zf.write('archivosGuardados/postproc')

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()
        prefer_options = self.question.prefer_options.all()
        options_ordering = self.question.options_ordering.all()
        candidates = self.candidates.all()
        escanios = self.escanios
        cnds = []
        for candidate in candidates:
            if isinstance(tally,list):
                votes = tally.count(candidate.number)
            else:
                votes=0
            cnds.append({
                'id':candidate.id,
                'sex': candidate.sex,
                'age': candidate.age,
                'political_party': candidate.political_party.abreviatura
            })
        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes,
                'escanio':escanios
            })
        prefers = []
        for pre in prefer_options:
            if isinstance(tally, list):
                votes = tally.count(pre.number)
            else:
                votes = 0
            prefers.append({
                'option': pre.option,
                'prefer_op': pre.prefer,
                'number': pre.number,
                'votes': votes
            })
        opts_ordering = []
        for opt in options_ordering:
            if isinstance(tally, list):
                votes = tally.count(opt.ordering)
            else:
                votes = 0
            opts_ordering.append({
                'option': opt.option,
                'ordering':opt.ordering,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts, 'options_ordering': opts_ordering , 'prefer_options':prefers,'candidates':cnds,'escanio':escanios}
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()
        #Aqui hacemos el guardado del postproc
        with open ('archivosGuardados/postproc','w') as f:
             for postprocs in json.dumps(self.postproc):
                 json.dump(postprocs,f)

    def __str__(self):
        return self.name

class ReadonlyVoting(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(null=True, max_length=100)
    question = models.ForeignKey(Question, related_name='readonly_voting', on_delete=models.CASCADE)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='readonly_voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='readonly_votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    # Comentamos lo que sigue porque pese a que esta preparado para funcionar, no se puede usar al no haber modificado la cabina de votaciones y el visualizer
    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    """ def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass
        
        self.tally = response.json()
        self.save()
        

        self.do_postproc()
        

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save() """
        
    def __str__(self):
        return self.name

class MultipleVoting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ManyToManyField(Question, related_name='multiple_voting')

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='multiple_voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='multiple_votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    # Comentamos lo que sigue porque pese a que esta preparado para funcionar, no se puede usar al no haber modificado la cabina de votaciones y el visualizer
    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    """ def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that 
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        question = self.question.all()

        qsts = []
        for qst in question:
            opts = []
            for opt in qst.options.all():
                if isinstance(tally, list):
                    votes = tally.count(opt.number)
                else:
                    votes = 0
                opts.append({
                    'option': opt.option,
                    'number': opt.number,
                    'votes': votes
                })
            qsts.append({'options': opts})
            
        data = { 'type': 'IDENTITY', 'question': qsts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save() """

    def __str__(self):
        return self.name