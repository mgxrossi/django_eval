from django.db import models

# Create your models here.
"""Data model of the skill exchange application."""

from django.conf import settings
from django.db import models


class Skill(models.Model):
    """hérite de models.Model
    Créé par l'admin dans l'admin site Django
    """

    name = models.CharField("nom", max_length=100, unique=True) #interdit deux compétences avec le même nom
    owners = models.ManyToManyField( #le lien possède de mon diagramme a 0..* des deux cotés donc Django créé une table de liaison cachée compétence ↔ utilisateur
        settings.AUTH_USER_MODEL, #désigne le User fourni par Django
        related_name="skills", #le nom du lien vu depuis l’utilisateur : je pourrais faire margaux.skills.all() pour avoir mes compétences.
        blank=True, #compétence pas obligatoire
        verbose_name="utilisateurs qui la possèdent",
    )

    class Meta:
        ordering = ["name"] #compétence par ordre alphabétique
        verbose_name = "compétence" #le nom affiché dans l'admin

    def __str__(self) -> str:
        return self.name
    #Quand tu crées une compétence, Django fabrique en mémoire un objet Python qui contient plusieurs infos or a plein d'endroits django doit l'afficher sousforme de texte
    #Il se dit : quel texte dois-je écrire pour représenter cette boîte ? Pour y répondre, il appelle la méthode __str__ de l’objet (« str » pour string) sinon python ne sait pas quelle info choisir dans la boite et par défaut il afficherait le nom de la classe et le num de l'objet
    #Ici on dit « pour représenter une compétence en texte, prends son nom ». self désigne l’objet lui-même, et self.name sa colonne name

class HelpRequest(models.Model):
    """un utilisateur qui cherche de l'aide sur un créneau précis soit un jour entier.
    une fois l'aidant engagée, la demande est validée
    commode entière avec son étiquette
    """

    requester = models.ForeignKey( #clé étrangère, chaque demande pointe vers un utilisateur
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, #Si l’utilisateur est supprimé, ses demandes le sont aussi
        related_name="help_requests", #ex : margaux.help_requests.all() donne mes demandes
        verbose_name="demandeur", ##le nom affiché dans l'admin, tiroir de la commode
    )
    skill = models.ForeignKey( #La demande porte sur une compétence
        Skill,
        on_delete=models.PROTECT, #Empêche de supprimer une compétence tant que des demandes l’utilisent
        related_name="help_requests",
        verbose_name="compétence", #autre tiroir de la commode, chacun son étiquette
    )

    activity = models.CharField("activité", max_length=200) #description libre de 200 caractères max
    date = models.DateField("date")
    helper = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="engagements", #ex : lucas.engagements.all() donne les demandes où il aide
        null=True, #null=True autorise la base à laisser la case vide, Parce qu’au moment où la demande est créée, personne ne s’est encore proposé pour aider
        blank=True, # blank=True autorise les formulaires à la laisser vide
        verbose_name="aidant", #tiroir de la commode HelpRequest
    )
    created_at = models.DateTimeField("créée le", auto_now_add=True)
    #Remplie automatiquement avec la date et l’heure de création

    class Meta:
        ordering = ["date"]
        verbose_name = "demande d'aide"
        verbose_name_plural = "demandes d'aide"
        constraints = [
            models.UniqueConstraint( #Impossible d’avoir deux lignes avec le même demandeur, la même compétence et la même date
                fields=["requester", "skill", "date"],
                name="unique_request_per_skill_and_day",
            ),
            models.UniqueConstraint( #Un aidant ne peut apparaître qu’une fois par date : un engagement par jour
                fields=["helper", "date"],
                condition=models.Q(helper__isnull=False),
                name="one_engagement_per_helper_and_day",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.date} – {self.skill} – {self.activity}"
    #Ici, on assemble plusieurs informations. Le f"…" permet d’insérer des valeurs entre accolades

    def is_booked(self) -> bool:
        #Renvoie True si quelqu’un s’est engagé
        return self.helper is not None