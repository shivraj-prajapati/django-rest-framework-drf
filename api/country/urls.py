from rest_framework.urls import path
from .views import CountryAPI, CountryDetailAPI

urlpatterns = [
    path('', CountryAPI, name='create-country-list'),
    path('<str:id>/', CountryDetailAPI, name='country-update-delete')
]
