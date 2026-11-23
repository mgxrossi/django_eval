"""formulaire d'inscription
Imports rangés en 3 groupes : python, django puis mon appli """

from datetime import timedelta # durée 183 jours, vient de python directement

from django import forms  #Va chercher la boîte à outils des formulaires de Django
from django.contrib.auth.forms import UserCreationForm #formulaire d’inscription fourni par Django
from django.contrib.auth.models import User #le modèle User de Django
from django.utils import timezone # pour connaître la date d'aujourd'hui, à l'heure de Paris
from .models import HelpRequest, Skill #va chercher mon modèle Skill dans le fichier models.py, parce que le formulaire doit proposer la liste des compétences, qui sont dans la table Skill

BOOKING_HORIZON_DAYS = 183 # 6 mois pour limiter le calendrier

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


class HelpRequestForm(forms.ModelForm): # 1) déclaration. Hérite de forms.ModelForm
    """demande d'aide sur un jour précis pour une compétence que l'utilisateur n'a pas lui meme
    quatre parties : la déclaration, la classe Meta (les reglages), __init__, et les règles de validation"""

    #2) les réglages
    class Meta:
        model = HelpRequest
        #se fabrique à partir du modèle HelpRequest. Django refuse de démarrer sans cette ligne, car un ModelForm doit savoir de quel modèle il part.
        fields = ["skill", "date", "activity"] #champs que l utilisateur pourra remplir
        labels = {"activity": "Activité (description libre)"} #dictionnaire : {nom du champ: nouvelle étiquette}
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "activity": forms.TextInput(attrs={"placeholder": "ex. : tailler un rosier"}), #texte d'exemple en gris
            #Change l'apparence de deux champs, sans toucher à leurs règles, avec calendrier cliquable par ex
        }

    #3)adapter le formulaire à l'utilisateur
    #on n'affiche que celles qu'il ne possède pas. Or la classe est écrite une fois pour tous. Il faut donc ajuster le formulaire au moment où on le crée
    #init methode que python appelle automatiquement a chaque créa d'objet, elle s'exécute à chaque HelpRequestForm(...) dans la vue.
    ##user l'argument en plus, soit l'utilisateur connecté
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["skill"].queryset = Skill.objects.exclude(owners=user) #liste des compétences moins les siennes
        today = timezone.localdate()
        last_day = today + timedelta(days=BOOKING_HORIZON_DAYS)
        self.fields["date"].widget.attrs.update(min=today.isoformat(), max=last_day.isoformat()) #ajoute deux attributs au calendrier : les jours avant min et après max sont grisés
       #On le fait dans __init__ et pas dans Meta, parce que la date change chaque jour et dans meta elle sera calculée une seule fois au démarrage du serveur.

    #4) Les regles de validation
    def clean_date(self):
        date = self.cleaned_data["date"]
        today = timezone.localdate()
        last_day = today + timedelta(days=BOOKING_HORIZON_DAYS)
        if not today <= date <= last_day:
            raise forms.ValidationError(
                f"Choisissez une date entre le {today:%d/%m/%Y} et le {last_day:%d/%m/%Y}."
                #Si la date n'est pas entre aujourd'hui et dans 6 mois », alors on refuse avec raise forms.ValidationError(...)
                #meme si le calendrier grise les dates tout ce qui vient du navigateur peut etre modifié donc la vraie vérification doit se faire toujours côté serveur.
            )
        return date #on rend la date à Django pour qu'il la garde sinon l enregistrement plante

    #clean : une règle sur plusieurs champs, sans nom de champ, appelée après toutes les méthodes clean_<champ>
    def clean(self):
        cleaned_data = super().clean()
        skill = cleaned_data.get("skill")
        date = cleaned_data.get("date")
        if skill and date and HelpRequest.objects.filter(
            requester=self.user, skill=skill, date=date
        ).exists():
            raise forms.ValidationError("Vous avez déjà une demande pour cette compétence ce jour-là.")
        # plusieurs demandes le même jour, mais pas sur la même compétence
        #skill and date : on ne vérifie que si les deux sont valides
        #on cherche une demande existante du même utilisateur (self.user, gardé dans __init__), même compétence, même date
        return cleaned_data