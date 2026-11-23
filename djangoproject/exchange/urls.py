"""URLs of the skill exchange application."""

from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
#Va chercher les vues de connexion fournies par Django. as auth_views leur donne un surnom, pour ne pas les confondre avec mes views

app_name = "exchange" #app_name crée un espace de noms : dans les gabarits, j'écrirai {% url 'exchange:dashboard' %}
urlpatterns = [
    #name= donne un nom à chaque adresse. Si je change un jour le chemin, aucun lien ne casse
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("skills/", views.my_skills, name="my_skills"), #la fonction qui va répondre, dans views.py et le nom de l'adresse, utilisé dans {% url 'exchange:my_skills' %}
    path("requests/new/", views.create_request, name="create_request"),
    path("requests/search/", views.search_requests, name="search"),
    path("requests/<int:pk>/offer/", views.offer_help, name="offer_help"),
    #Cette adresse a une partie qui change : <int:pk>. C'est le numéro de la demande sur laquelle on clique
    path("login/", auth_views.LoginView.as_view(), name="login"), #La vue toute faite qui affiche le formulaire de connexion
                                             # Ces vues de Django sont des classes, pas des fonctions .as_view() les transforme en quelque chose que path() sait utiliser
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), #La vue toute faite qui déconnecte l’utilisateur
]