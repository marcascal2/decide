from django.contrib import admin
from django.utils import timezone

from .models import QuestionOption
from .models import QuestionPrefer
from .models import QuestionOrdering
from .models import Question
from .models import Party
from .models import Voting, ReadonlyVoting, MultipleVoting
from .models import Candidate
from django.core.exceptions import ValidationError


from .filters import StartedFilter

def confirm_date(modeladmin, request, queryset):
    for v in queryset.all():
        if v.start_date is None:
            raise ValidationError("La fecha inicio no puede ser confirmada si no existe")
        elif v.start_date < timezone.now():
            raise ValidationError("La fecha no puede ser anterior a ahora")
        else:
            v.create_pubkey()
            v.save()

def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption

class QuestionPreferInLine(admin.TabularInline):
    model= QuestionPrefer

class QuestionOrderingInline(admin.TabularInline):
    model = QuestionOrdering
   
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]
    inlines = [QuestionOptionInline, QuestionPreferInLine, QuestionOrderingInline]


# class CandidateAdmin(admin.ModelAdmin):
#     list_display = ('name', 'sex',)


# class QuestionCandidateAdmin(admin.ModelAdmin):
#     list_display = ('political_party',)

class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'min_age', 'max_age')
    readonly_fields = ('pub_key', 'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ,confirm_date ]  

class ReadonlyVotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=None, **kwargs)

        if obj is not None:

            form.base_fields["desc"].disabled = True
            form.base_fields["name"].disabled = True
            form.base_fields["question"].disabled = True
            form.base_fields["auths"].disabled = True

        return form

    actions = [ start, stop ]
# class VotingCandidateAdmin(admin.ModelAdmin):
#     list_display = ('name', 'start_date', 'end_date')
#     readonly_fields = ('start_date', 'end_date', 'pub_key',
#                        'tally', 'postproc')
#     date_hierarchy = 'start_date'
#     list_filter = (StartedFilter,)
#     search_fields = ('name', )

class MultipleVotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop ]


admin.site.register(Voting, VotingAdmin)
admin.site.register(MultipleVoting, MultipleVotingAdmin)
admin.site.register(ReadonlyVoting, ReadonlyVotingAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Candidate)
admin.site.register(Party)
# admin.site.register(VotingCandidate, VotingCandidateAdmin)
# admin.site.register(QuestionCandidate,QuestionCandidateAdmin)
