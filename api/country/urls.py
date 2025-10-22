from rest_framework.urls import path
from .views import CountryAPI

urlpatterns = [
    path('', CountryAPI, name='create-country-list'),
]
