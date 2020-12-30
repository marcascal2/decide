from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('<int:census_group_by_voter_id>/', views.CensusGroupVoter.as_view(), name='census_voter_detail'),
]
