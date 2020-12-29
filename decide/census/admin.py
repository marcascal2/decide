from django.contrib import admin

from .models import Census
from voting.models import Voting

class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting', 'voter','adscripcion','date')
    list_filter = ('voting', 'adscripcion','date','voting__question')

    search_fields = ('voter', 'adscripcion')

    

admin.site.register(Census, CensusAdmin)
