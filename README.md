# Projet Pokedex

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


## Fonctionnement du jeu
### 1. Pokedex
Lorsque le joueur accède à la page principale du Pokedex, il voit une liste de 150 Pokémon qu'il peut parcourir. Il peut rechercher un Pokémon par son nom (en français) et ajouter des Pokémon à son équipe.

### 2. Gestion de l'équipe
Le joueur peut gérer son équipe en ajoutant ou en supprimant des Pokémon depuis le Pokedex. L'équipe peut contenir jusqu'à 6 Pokémon.

### 3. Combat
Lorsque l'équipe est prête, le joueur peut commencer un combat contre une équipe d'IA générée aléatoirement. Le combat se déroule au tour par tour, où chaque Pokémon attaque ou change de Pokémon en fonction de ses actions.

L'IA choisit de manière aléatoire entre attaquer ou changer de Pokémon en fonction de ses PV. Les dégâts sont calculés en fonction des statistiques des Pokémon (Attaque, Défense, PV).

### 4. Résultats
Après chaque combat, le jeu affiche le gagnant (le joueur ou l'IA) et un résumé détaillé du combat, y compris les actions effectuées et les Pokémon KO.
