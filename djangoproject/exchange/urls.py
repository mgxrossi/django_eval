"""URLs of the skill exchange application."""

from django.urls import path

from . import views

app_name = "exchange" #app_name crée un espace de noms : dans les gabarits, j'écrirai {% url 'exchange:dashboard' %}
urlpatterns = [
    #name= donne un nom à chaque adresse. Si je change un jour le chemin, aucun lien ne casse
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("skills/", views.my_skills, name="my_skills"),
    path("requests/new/", views.create_request, name="create_request"),
    path("requests/search/", views.search_requests, name="search"),
    path("requests/<int:pk>/offer/", views.offer_help, name="offer_help"),
]