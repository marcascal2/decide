from django.contrib import admin

from .models import Census, CensusGroupByVoting
from voting.models import Voting

class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting', 'voter','adscripcion','date')
    list_filter = ('voting', 'adscripcion','date','voting__question')

    search_fields = ('voter', 'adscripcion')

class CensusGroupByVotingAdmin(admin.ModelAdmin):
    list_display = ('voting', 'census_number')
    readonly_fields = ('census_number', ) 

admin.site.register(Census, CensusAdmin)
admin.site.register(CensusGroupByVoting, CensusGroupByVotingAdmin)