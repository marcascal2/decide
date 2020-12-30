from rest_framework import serializers

from .models import Question, QuestionOption, Voting, QuestionCandidate, Candidate
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
# class CandidateSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Candidate
#         fields = ('name', 'age', 'sex', 'auto_community')
# class QuestionCandidateSerializer(serializers.HyperlinkedModelSerializer):
#     options = CandidateSerializer(many=True)
#     class Meta:
#         model = QuestionCandidate
#         fields = ('political_party','options')

class VotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    # candidates =  QuestionCandidateSerializer(many=True)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'start_date', 'candidates',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')

class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')
