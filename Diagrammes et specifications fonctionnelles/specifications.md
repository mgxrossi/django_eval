# Spécifications fonctionnelles – Échange de compétences

## II. Spécifications fonctionnelles

En réponse aux besoins exprimés par le client, l'application web a été spécifiée sur la base des fonctionnalités suivantes, accessibles par les acteurs concernés :

**UC1 – Afficher les prochains créneaux réservés**
Affiche à tout visiteur, sur la page d'accueil, la liste des prochains créneaux (à partir du jour même) pour lesquels un utilisateur s'est rendu disponible pour aider un autre utilisateur, en précisant pour chacun d'eux la date et la compétence concernée. L'affichage est anonyme : aucun nom ni aucune information personnelle n'est indiqué (ex. : « Un utilisateur a proposé son aide en jardinage à un autre utilisateur le 23 novembre 2026 »).

**UC2 – Afficher la liste des compétences**
Affiche à tout visiteur, sur la page d'accueil, la liste des compétences que l'application propose à ses utilisateurs d'échanger.

**UC3 – S'inscrire**
Permet à un visiteur de créer un compte utilisateur en renseignant un identifiant, son prénom, son nom, son adresse de courriel et un mot de passe (saisi deux fois pour confirmation). Ces informations sont toutes obligatoires ; le prénom, le nom et le courriel seront visibles des seuls utilisateurs avec qui il échangera. Une fois le compte créé, le visiteur est redirigé vers la page de connexion (UC4).

**UC4 – Se connecter**
Permet à un visiteur de se connecter en renseignant son identifiant et son mot de passe. Une fois connecté, il accède à son espace utilisateur (UC10) et aux fonctionnalités réservées aux utilisateurs.

**UC5 – Se déconnecter**
Permet à un utilisateur connecté de se déconnecter à tout moment depuis le bandeau du site ; il redevient alors visiteur et est redirigé vers la page d'accueil.

**UC6 – Gérer ses compétences**
Permet à un utilisateur d'indiquer, parmi la liste des compétences, celles qu'il possède et est prêt à offrir, en les cochant, et de retirer celles qu'il ne souhaite plus offrir. Une compétence ne peut pas être retirée tant que l'utilisateur est engagé à aider quelqu'un sur un créneau à venir pour cette compétence : un message s'affiche alors pour l'informer que la suppression est impossible car il a des engagements en cours.

**UC7 – Demander de l'aide**
Permet à un utilisateur de demander de l'aide en sélectionnant une compétence parmi celles qu'il ne possède pas, en choisissant un jour dans un calendrier (entre aujourd'hui et dans 6 mois) et en décrivant librement l'activité concernée (ex. : « tailler un rosier »). Une demande porte sur une seule journée ; un utilisateur peut faire plusieurs demandes le même jour, mais pour des compétences différentes. Une demande ne peut pas être annulée dans cette version : les utilisateurs s'arrangent entre eux par courriel.

**UC8 – Rechercher des demandes d'aide**
Permet à un utilisateur d'afficher les prochaines demandes d'aide des autres utilisateurs, en les filtrant au moyen d'un formulaire composé d'une liste déroulante de ses compétences, d'un calendrier pour choisir une date et d'un bouton « Rechercher ». Ne sont affichées que les demandes à venir qui portent sur une compétence qu'il possède et pour lesquelles personne ne s'est encore engagé. Pour chacune sont indiqués la date, la compétence, l'activité et le nom du demandeur.

**UC9 – Se rendre disponible pour une demande**
Permet à un utilisateur, depuis UC8, après sélection d'une des demandes de la liste affichée, de s'engager à aider le demandeur ce jour-là. L'engagement est immédiat et définitif : le demandeur n'a pas à l'accepter, et la demande n'est plus proposée à aucun autre utilisateur. Un utilisateur ne peut s'engager que sur une seule demande par jour.

**UC10 – Consulter son récapitulatif**
Affiche à un utilisateur, sur sa page d'accueil, le récapitulatif de ses prochaines demandes d'aide et de ses prochains engagements. Pour chacun sont indiqués la date, la compétence et l'activité, ainsi que le prénom, le nom et l'adresse de courriel de l'autre personne, afin qu'ils puissent s'organiser. Une demande sans aidant est signalée « en attente d'un aidant ».

**UC11 – Gérer les compétences et les utilisateurs**
Permet à l'administrateur, depuis le site d'administration de Django, de créer, modifier ou supprimer les compétences proposées par l'application ainsi que les comptes utilisateurs. Il peut également consulter les demandes d'aide et les engagements.

