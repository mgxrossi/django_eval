"""Views of the skill exchange application."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

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