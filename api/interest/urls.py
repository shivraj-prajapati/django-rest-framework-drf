from rest_framework.urls import path
from .views import InterestAPI, InterestDetailAPI

urlpatterns = [
    path('', InterestAPI, name='create-intrest-list'),
    path('<str:id>/', InterestDetailAPI, name='interest-update-delete')
    
]
