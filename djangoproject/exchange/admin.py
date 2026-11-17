#L'admin gère les compétences et demandes

from django.contrib import admin #Va chercher l’outil admin dans Django

from .models import HelpRequest, Skill #Va chercher mes classes HelpRequest et Skill dans le fichier models.py


@admin.register(Skill) #comme un tampon qui dit inscris Skill dans l’admin, en utilisant cette fiche de réglages
class SkillAdmin(admin.ModelAdmin): #crée une fiche de réglages pour l’affichage des compétences dans l’admin, admin.ModelAdmin est le modèle de fiche que fournit Django puis on modifie ce qu'on veut ensuite

#Viennent ensuite les réglages. Chacun est une liste entre crochets [ ], qui contient des noms de champs de mon modèle.
    list_display = ["name"] #Quelles colonnes afficher dans la liste. Ici juste le nom
    search_fields = ["name"] #Ajoute une barre de recherche qui cherche dans le nom
    filter_horizontal = ["owners"] #Avec le réglage : deux listes tu passes un à l'autre comme ca pas d'erreur et pas beosin de faire CTRL pour en selectionner plusieurs


#Même principe : une fiche de réglages pour les demandes d’aide, tamponnée pour inscrire HelpRequest dans l’admin
@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    """demande d'aide et aidant"""

    list_display = ["date", "skill", "activity", "requester", "helper"] #un vrai tableau
    list_filter = ["skill", "date"] #Ajout de filtres dans une colonne à droite : clic sur « Jardinage » pour ne voir que les demandes de jardinage, ou sur « Ce mois-ci » pour les dates par exemple
    search_fields = ["activity"] #Barre de recherche dans les descriptions d’activité