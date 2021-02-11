from rest_framework import serializers

from .models import Question, Party, Plank, Program, QuestionOption, Voting, QuestionPrefer, QuestionOrdering, Candidate, ReadonlyVoting, MultipleVoting
from base.serializers import KeySerializer, AuthSerializer


class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('number', 'option')

class QuestionOrderingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOrdering
        fields = ('ordering','number', 'option')

class QuestionPreferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionPrefer
        fields = ('prefer','number', 'option')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)
    prefer_options = QuestionPreferSerializer(many=True)
    options_ordering = QuestionOrderingSerializer(many=True)
    class Meta:
        model = Question
        #fields = ('desc', 'options')
        fields = ('prefer_options','desc', 'options', 'options_ordering')

class PlankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plank
        fields = ('number', 'plank')

class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    planks = PlankSerializer(many=True)
    class Meta:
        model = Program
        fields = ('title', 'overview', 'planks')

class PartySerializer(serializers.HyperlinkedModelSerializer):
    program = ProgramSerializer(many=False)
    class Meta:
        model = Party
        fields = ('abreviatura','nombre', 'program')




class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    political_party = PartySerializer(many=False)
    class Meta:
        model = Candidate
        fields = ('number', 'name', 'age', 'sex', 'auto_community', 'political_party' )

class VotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)
    candidates = CandidateSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'start_date', 'candidates', 'escanios',
                  'end_date', 'min_age', 'max_age', 'pub_key', 'auths', 'customURL', 'tally', 'postproc')

class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date', 'min_age', 'max_age','customURL')

class ReadonlyVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = ReadonlyVoting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')

class ReadonlySimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = ReadonlyVoting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')

class MultipleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=True)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = MultipleVoting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')

class MultipleSimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=True)

    class Meta:
        model = MultipleVoting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')
