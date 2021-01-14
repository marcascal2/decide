from django.urls import path
from .views import BoothView
from .views import BoothViewCustom


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('<str:customURL>/', BoothViewCustom.as_view()),
]
