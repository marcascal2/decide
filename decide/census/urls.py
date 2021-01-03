from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admin/', views.adminView, name='admin_census_panel'),
]
