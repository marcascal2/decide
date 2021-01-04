from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('all_census/',views.all_census, name='all_census'),
    path('group_by_voting/<int:voting_id>',views.group_by_voting, name='group_by_voting'),
    path('group_by_voter/<int:voter_id>',views.group_by_voter, name='group_by_voter'),
    path('group_by_date/<str:date>',views.group_by_date, name='group_by_date'),
    path('group_by_adscripcion/<str:adscripcion>',views.group_by_adscripcion, name='group_by_adscripcion'),
    path('group_by_question/<str:question>',views.group_by_question, name='group_by_question')
]
