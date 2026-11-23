"""Views of the skill exchange application"""

from django.contrib.auth.decorators import login_required #réserver la page aux utilisateurs connectés
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render #render affiche le gabarit ; redirect envoie vers une autre page
from django.utils import timezone #connaître la date d'aujourd'hui, pour savoir si un engagement est à venir
from django.contrib import messages #afficher « Vos compétences ont été enregistrées » par ex
from .forms import HelpRequestForm, SignUpForm, SkillsForm

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


@login_required #une espece de garde comme ca si la personne n'est pas connectée la vue ne s’exécute pas
def dashboard(request: HttpRequest) -> HttpResponse:
    """User home page: summary of his requests and engagements."""
    user = request.user #L’utilisateur connecté qui demande la page. On le range dans une variable plus courte
    today = timezone.localdate()
    context = {
        "my_skills": user.skills.all(), #skills est le related_name du ManyToManyField dans ton modèle Skill
        "my_requests": user.help_requests.filter(date__gte=today).select_related("skill", "helper"), #C’est le related_name du champ requester
        "my_engagements": user.engagements.filter(date__gte=today).select_related("skill", "requester"), #C’est le related_name du champ helper
    }
    #pour le filtre : seulement celles d’aujourd’hui ou plus tard
    #select_related( , ) c'est pour récupèrer en une seule fois la compétence et l’aidant de chaque demande et éviter plusieurs requetes
    return render(request, "exchange/dashboard.html", context)


@login_required
def my_skills(request: HttpRequest) -> HttpResponse: #La fonction reçoit la requête du navigateur et renvoie une réponse
    #Le nom my_skills : exactement celui écrit dans urls.py (views.my_skills)
    user = request.user  #L'utilisateur connecté, rangé dans une variable plus courte, car on va s'en servir souvent
    if request.method == "POST":  #lié aux cases que l'utilisateur a cochées
        form = SkillsForm(request.POST)
        if form.is_valid():
            selected = set(form.cleaned_data["skills"])
            #cleaned_data["skills"] contient les compétences cochées, déjà transformées en objets et set(…) les range dans un ensemble (collection sans doublons, sur laquelle on peut faire des soustractions)
            removed = set(user.skills.all()) - selected #ce qu'il possédait avant moins ce qu'il a coché maintenant
            today = timezone.localdate()
            busy = user.engagements.filter(date__gte=today, skill__in=removed) #pour pas retirer compétences alors qu'il a un engagement dessus
            if busy.exists():
                names = ", ".join(sorted({slot.skill.name for slot in busy})) #fabrique la liste des compétences bloquées pour le message d'alerte
                messages.error(
                    request,
                    f"Suppression impossible : vous avez des engagements en cours pour : {names}.",
                )
                return redirect("exchange:my_skills")
            # recharge plutot que réaffiche donc repasse par le get et affiche les cases cochées avant le retrait
            user.skills.set(selected)
            #Si aucune compétence n'est bloquée, on enregistre.
            messages.success(request, "Vos compétences ont été enregistrées.")
            return redirect("exchange:dashboard")
            #Le message vert, puis la redirection vers « Mon espace »

    else:
        #On crée un formulaire non lié avec les compétences qu'il a déja.
        form = SkillsForm(initial={"skills": user.skills.all()})
    return render(request, "exchange/my_skills.html", {"form": form})
#On affiche le gabarit, en lui donnant le formulaire sous le nom form. C'est ce nom qu'on écrira dans le HTML : {{ form.as_div }}
#Si form c'est invalide, on saute directement au return render(...)


#C'est le même schéma GET / POST que Mes compétences

@login_required
def create_request(request: HttpRequest) -> HttpResponse:
    """Demande d'aide sur un jour précis, pour une compétence que l'utilisateur n'a pas"""
    if request.method == "POST":
        form = HelpRequestForm(request.POST, user=request.user)
        if form.is_valid():
            help_request = form.save(commit=False)
            help_request.requester = request.user
            help_request.save()
            messages.success(request, "Votre demande d'aide a été enregistrée.")
            return redirect("exchange:dashboard")
    else:
        form = HelpRequestForm(user=request.user)
    return render(request, "exchange/request_form.html", {"form": form})


def search_requests(request: HttpRequest) -> HttpResponse:
    """Search open help requests matching the user's skills."""
    return HttpResponse("Rechercher des demandes")


def offer_help(request: HttpRequest, pk: int) -> HttpResponse:
    """Commit the user to help on request number pk."""
    return HttpResponse(f"Se rendre disponible pour la demande {pk}")