from django.shortcuts import render

# Create your views here

"""Views of the skill exchange application."""

from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """Home page: booked slots (anonymous) and list of skills."""
    return HttpResponse("Accueil")


def signup(request: HttpRequest) -> HttpResponse:
    """Create a user account."""
    return HttpResponse("Inscription")


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