from django.contrib import admin

from .models import Census, CensusGroupByVoting, CensusGroupByVoter
from voting.models import Voting

class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting', 'voter','adscripcion','date')
    list_filter = ('voting', 'voter','adscripcion','date','voting__question')

    search_fields = ('voter', 'adscripcion')

class CensusGroupByVotingAdmin(admin.ModelAdmin):
    list_display = ('voting', 'census_number')
    readonly_fields = ('census_number', 'census') 

class CensusGroupByVoterAdmin(admin.ModelAdmin):
    list_display = ('voter', 'census_number',)
    readonly_fields = ('census_number', 'census') 

admin.site.register(Census, CensusAdmin)
admin.site.register(CensusGroupByVoting, CensusGroupByVotingAdmin)
admin.site.register(CensusGroupByVoter, CensusGroupByVoterAdmin)