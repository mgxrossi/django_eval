"""formulaire d'inscription"""

from django import forms
from django.contrib.auth.forms import UserCreationForm #formulaire d’inscription fourni par Django
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm): #crée notre formulaire à partir de celui de Django, on rajoute ce qu'il manque = héritage
    """Account creation, with the information shown to other users."""

#tous obligatoires!
    first_name = forms.CharField(label="Prénom", max_length=150) #label est l’étiquette affichée
    last_name = forms.CharField(label="Nom", max_length=150)
    email = forms.EmailField(label="Adresse de courriel") #Django vérifie tout seul qu’il ressemble à une adresse avec un @

    class Meta(UserCreationForm.Meta): #réglages du formulaire. On part de ceux de Django, puis on les complète
        model = User #le formulaire remplit un objet User
        fields = ("username", "first_name", "last_name", "email") #les champs à afficher, dans cet ordre