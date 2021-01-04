from rest_framework import serializers

from .models import Question, QuestionOption, Voting, MultipleVoting
from base.serializers import KeySerializer, AuthSerializer


class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('number', 'option')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('desc', 'options')


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')


class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
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