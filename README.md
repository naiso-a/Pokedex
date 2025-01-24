# Pokémon Battle Game

Ce projet est un jeu de combat Pokémon développé en Django, permettant à un joueur de créer son équipe, de choisir des Pokémon et de combattre contre une équipe de l'IA. Le jeu récupère des informations sur les Pokémon via l'API de PokéAPI et permet au joueur d'interagir avec le jeu via une interface web.

## Fonctionnalités

- **Pokedex** : Affiche une liste de Pokémon avec leur nom et image. Permet au joueur de rechercher des Pokémon par nom et d'ajouter des Pokémon à son équipe.
- **Équipe** : Permet au joueur de gérer son équipe, d'ajouter ou de supprimer des Pokémon.
- **Combat** : Le joueur affronte une équipe d'IA dans un combat au tour par tour. Chaque Pokémon a des statistiques (PV, Attaque, Défense) qui influencent les combats.
- **Journal de combat** : Un journal enregistre chaque action pendant le combat (attaques, changements de Pokémon, Pokémon KO).
- **Affichage des résultats** : Après un combat, le jeu affiche qui a gagné (le joueur ou l'IA) et un résumé du combat.

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Django 3.x
- Une connexion Internet pour récupérer les données des Pokémon via PokéAPI

### Installation des dépendances

1. Clone ce dépôt :
   ```bash
   git clone https://github.com/ton-utilisateur/ton-repository.git
   cd ton-repository
Crée un environnement virtuel et active-le :

bash
Copier
Modifier
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
Installe les dépendances nécessaires :

bash
Copier
Modifier
pip install -r requirements.txt
Lance les migrations pour configurer la base de données :

bash
Copier
Modifier
python manage.py migrate
Lance le serveur de développement :

bash
Copier
Modifier
python manage.py runserver
Accède au jeu en ouvrant http://127.0.0.1:8000 dans ton navigateur.
