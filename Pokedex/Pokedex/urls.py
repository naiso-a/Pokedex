"""
URL configuration for Pokedex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from pokeapp import views

urlpatterns = [
    path('', views.pokedex, name='pokedex'),
    path('pokemon/<str:name>/', views.pokemon_detail, name='pokemon_detail'),
    path('team/', views.team_view, name='team_view'),
    path('battle/', views.battle_view, name='battle_view'),
    path('turn/', views.process_turn, name='process_turn'),

]   