from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='senti-home'),
    path('search/', views.search, name='senti-tweets'),
]
