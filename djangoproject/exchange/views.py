"""Views of the skill exchange application."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib import messages
from .forms import SignUpForm

from .models import HelpRequest, Skill

def index(request: HttpRequest) -> HttpResponse:
    """page d'accueil avec demandes déja créées et compétences"""
    today = timezone.localdate()
    booked_slots = HelpRequest.objects.filter(
        date__gte=today, helper__isnull=False
    ).select_related("skill")
    skills = Skill.objects.all()
    context = {"booked_slots": booked_slots, "skills": skills}
    return render(request, "exchange/index.html", context)


#structure classique de toute vue avec un formulaire
#on arrive sur la page, le navigateur fait un GET, donc on passe dans le else. On crée un formulaire vide (SignUpForm()) et on affiche la page avec ce formulaire
#on clique sur « S’inscrire », le navigateur envoie les données en POST
def signup(request: HttpRequest) -> HttpResponse:
    """Create an account, then send the new user to the login page."""
    if request.method == "POST":
        form = SignUpForm(request.POST) #crée un formulaire rempli avec ce que l’utilisateur a tapé
        if form.is_valid(): #Django vérifie tout
            form.save() #Si tout est bon, on enregistre le nouvel utilisateur dans la base. Le mot de passe est chiffré automatiquement
            messages.success(request, "Votre compte a été créé. Vous pouvez vous connecter.") #On prépare un message à afficher sur la page suivante
            return redirect("exchange:login") #envoie l’utilisateur vers la page de connexion
    else:
        form = SignUpForm() #si pas valide on remet le formulaire
    return render(request, "exchange/signup.html", {"form": form})


def dashboard(request: HttpRequest) -> HttpResponse:
    """User summary: his requests and engagements."""
    return HttpResponse("Mon espace")


def my_skills(request: HttpRequest) -> HttpResponse:
    """Choose the skills the user owns."""
    return HttpResponse("Mes compétences")


def create_request(request: HttpRequest) -> HttpResponse:
    """Ask for help on a day for a skill the user does not own."""
    return HttpResponse("Demander de l'aide")


def search_requests(request: HttpRequest) -> HttpResponse:
    """Search open help requests matching the user's skills."""
    return HttpResponse("Rechercher des demandes")


def offer_help(request: HttpRequest, pk: int) -> HttpResponse:
    """Commit the user to help on request number pk."""
    return HttpResponse(f"Se rendre disponible pour la demande {pk}")