"""formulaire d'inscription"""

from django import forms  #Va chercher la boîte à outils des formulaires de Django
from django.contrib.auth.forms import UserCreationForm #formulaire d’inscription fourni par Django
from django.contrib.auth.models import User #le modèle User de Django
from .models import Skill #va chercher mon modèle Skill dans le fichier models.py, parce que le formulaire doit proposer la liste des compétences, qui sont dans la table Skill


class SignUpForm(UserCreationForm): #crée notre formulaire à partir de celui de Django, on rajoute ce qu'il manque = héritage
    """Account creation, with the information shown to other users."""

#tous obligatoires!
    first_name = forms.CharField(label="Prénom", max_length=150) #label est l’étiquette affichée
    last_name = forms.CharField(label="Nom", max_length=150)
    email = forms.EmailField(label="Adresse de courriel") #Django vérifie tout seul qu’il ressemble à une adresse avec un @

    class Meta(UserCreationForm.Meta): #réglages du formulaire. On part de ceux de Django, puis on les complète
        model = User #le formulaire remplit un objet User
        fields = ("username", "first_name", "last_name", "email") #les champs à afficher, dans cet ordre



class SkillsForm(forms.Form):
    """les compétences que l'utilisateur est prêt à offrir
    SkillsForm c ets le nom du nouveau type d'objet
    il hérite de forms.Form : il récupère tout ce que sait faire un formulaire Django
    """

    skills = forms.ModelMultipleChoiceField(
        #un seul champ, qu’on appelle skills. Ce nom est important : c’est lui qu’on retrouvera
        #dans la vue : form.cleaned_data["skills"] ;
        #dans le HTML : name="skills", et l’identifiant id_skills utilisé par ton CSS
        #les choix viennent d’un modèle (une table) et on peut en choisir plusieurs, c'est un champ à choix (ChoiceField)
        label="Mes compétences", #Sans label Django invente l'étiquette à partir du nom du champ et affiche « Skills »
        queryset=Skill.objects.all(), #La liste des choix proposé
        widget=forms.CheckboxSelectMultiple, #La façon de l’afficher, une case à cocher par compétence, bien plus claire que d'appuer sur CTRL pour en selectionner plusieurs etc
        required=False, #champ non obligatoire
        help_text="Cochez les compétences que vous êtes prêt(e) à offrir.", #pour guider l'utilisateur
    )


