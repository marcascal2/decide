from django.contrib import admin

from .models import Census
from voting.models import Voting

class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_name', 'voter_username','adscripcion','date')
    list_filter = ('voting_id', 'voter_id','adscripcion','date')

    search_fields = ('voter', 'adscripcion')

admin.site.register(Census, CensusAdmin)