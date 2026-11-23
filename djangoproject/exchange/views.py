"""Views of the skill exchange application"""

from django.contrib.auth.decorators import login_required #réserver la page aux utilisateurs connectés
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render #render affiche le gabarit ; redirect envoie vers une autre page ; retrouver la demande à partir de son numéro, ou afficher une page « 404 introuvable »
from django.views.decorators.http import require_POST #un garde qui n'accepte que les clics sur un bouton
from django.utils import timezone #connaître la date d'aujourd'hui, pour savoir si un engagement est à venir
from django.contrib import messages #afficher « Vos compétences ont été enregistrées » par ex
from .forms import HelpRequestForm, HelpSearchForm, SignUpForm, SkillsForm

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


@login_required
def search_requests(request: HttpRequest) -> HttpResponse:
    """Open help requests of other users, for the skills of the user."""
    user = request.user
    today = timezone.localdate()
    results = (
        HelpRequest.objects.filter(
            date__gte=today, helper__isnull=True, skill__in=user.skills.all()
        )
        .exclude(requester=user)
        .select_related("skill", "requester")
    )
    form = HelpSearchForm(request.GET or None, user=user)
    if form.is_valid():
        if form.cleaned_data["skill"]:
            results = results.filter(skill=form.cleaned_data["skill"])
        if form.cleaned_data["date"]:
            results = results.filter(date=form.cleaned_data["date"])
    return render(request, "exchange/search.html", {"form": form, "results": results})


@login_required
@require_POST
def offer_help(request: HttpRequest, pk: int) -> HttpResponse:     #La vue reçoit la requête et pk, le numéro lu dans l'adresse
    """engage l utilisateur sur une demande en particulier"""
    help_request = get_object_or_404(HelpRequest, pk=pk) #Va chercher dans la table HelpRequest la demande qui porte ce numéro
    user = request.user

    error = None #variable error, vide au départ, ensuite une serie de questions
    if help_request.requester == user:
        error = "Vous ne pouvez pas répondre à votre propre demande."
    elif not user.skills.filter(pk=help_request.skill_id).exists():
        error = "Vous ne possédez pas la compétence demandée."
    elif help_request.date < timezone.localdate():
        error = "Ce créneau est passé."
    elif user.engagements.filter(date=help_request.date).exists():
        error = "Vous êtes déjà engagé(e) sur un autre créneau ce jour-là."

    if error:
        messages.error(request, error)
        return redirect("exchange:search")
    #Si un message d'erreur a été écrit on l'affiche en rouge, et on renvoie l'utilisateur vers la recherche. Rien n'est enregistré

    updated = HelpRequest.objects.filter(pk=pk, helper__isnull=True).update(helper=user)
    #par ex : prends la demande n°12, seulement si sa case aidant est encore vide
    #.update(helper=user) : et écris le nom de l'utilisateur dans la case aidant ;
    if updated == 0:
        #Django répond combien de lignes il a modifiées : 1 si ça a marché, 0 sinon
        messages.error(request, "Ce créneau vient d'être pris par un autre utilisateur.")
        return redirect("exchange:search")

    messages.success(
        request,
        f"C'est noté : vous aidez {help_request.requester.first_name} le {help_request.date:%d/%m/%Y}.",
    )
    return redirect("exchange:dashboard")