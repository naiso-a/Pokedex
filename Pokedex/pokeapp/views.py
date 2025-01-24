from django.core.cache import cache
import requests
from django.shortcuts import render, redirect
import random
from django.shortcuts import render
from .models import Pokemon

# Vue principale pour afficher le Pokedex et gérer les équipes
def pokedex(request):
    search_query = request.GET.get('search', '').lower()  # Récupère la requête de recherche si elle existe
    pokemons = cache.get('translated_pokemons')  # Vérifie si les pokémons traduits sont en cache
    team = request.session.get('team', [])  # Récupère l'équipe du joueur depuis la session

    if not pokemons:  # Si les pokémons ne sont pas en cache, on les charge depuis l'API
        api_url = "https://pokeapi.co/api/v2/pokemon?limit=150"
        response = requests.get(api_url)
        if response.status_code == 200:  # Si la réponse de l'API est valide
            pokemons = response.json()['results']  # Récupère la liste des pokémons
            translated_pokemons = []  # Liste pour stocker les pokémons traduits

            # Pour chaque pokémon, on récupère sa traduction en français et son image
            for pokemon in pokemons:
                name = pokemon['name']
                species_url = f"https://pokeapi.co/api/v2/pokemon-species/{name}"
                sprite_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
                species_response = requests.get(species_url)
                sprite_response = requests.get(sprite_url)

                # Si on peut récupérer les informations de l'espèce et de l'image
                if species_response.status_code == 200 and sprite_response.status_code == 200:
                    species_data = species_response.json()
                    sprite_data = sprite_response.json()
                    french_name = next(
                        (n['name'] for n in species_data['names'] if n['language']['name'] == 'fr'),
                        name  # Si la traduction n'existe pas, on garde le nom en anglais
                    )
                    translated_pokemons.append({
                        'name': french_name,
                        'image_url': sprite_data.get('sprites', {}).get('front_default', None),  # URL de l'image du sprite
                        'english_name': pokemon['name'],
                    })
            cache.set('translated_pokemons', translated_pokemons, timeout=3600)  # Cache les pokémons pour 1 heure
        else:
            translated_pokemons = []  # Si l'API échoue, une liste vide est utilisée
    else:
        translated_pokemons = pokemons  # Sinon, on récupère les pokémons depuis le cache

    # Marque chaque pokémon pour savoir s'il est dans l'équipe du joueur
    for pokemon in translated_pokemons:
        pokemon['in_team'] = pokemon['name'] in team

    # Ajoute un pokémon à l'équipe si demandé
    if 'add' in request.GET:
        pokemon_name = request.GET.get('add')
        if pokemon_name not in team and len(team) < 6:  # Limite à 6 pokémons dans l'équipe
            team.append(pokemon_name)
        request.session['team'] = team

    # Retire un pokémon de l'équipe si demandé
    if 'remove' in request.GET:
        pokemon_name = request.GET.get('remove')
        if pokemon_name in team:
            team.remove(pokemon_name)
        request.session['team'] = team

    # Applique le filtre de recherche
    if search_query:
        translated_pokemons = [
            p for p in translated_pokemons if search_query in p['name'].lower()
        ]

    return render(request, 'pokedex.html', {
        'pokemons': translated_pokemons,  # Liste des pokémons à afficher
        'team': team,  # Équipe du joueur
    })


# Vue pour afficher l'équipe du joueur
def team_view(request):
    # Supprimer un Pokémon spécifique de l'équipe
    remove_pokemon = request.GET.get('remove_pokemon')
    if remove_pokemon:
        team = request.session.get('team', [])
        if remove_pokemon in team:
            team.remove(remove_pokemon)
            request.session['team'] = team
        return redirect('team_view')  # Redirige après la suppression

    # Charge les données des pokémons et filtre selon l'équipe
    pokemons = cache.get('translated_pokemons', [])
    team_names = request.session.get('team', [])
    team = [pokemon for pokemon in pokemons if pokemon['name'] in team_names]

    return render(request, 'team.html', {'team': team})  # Affiche l'équipe du joueur


# Vue pour afficher les détails d'un Pokémon
def pokemon_detail(request, name):
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{name}"
    sprite_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    species_response = requests.get(species_url)
    sprite_response = requests.get(sprite_url)
    if species_response.status_code == 200 and sprite_response.status_code == 200:
        species_data = species_response.json()
        sprite_data = sprite_response.json()
        image_url = sprite_data.get('sprites', {}).get('front_default', None)
        french_name = next(
            (name['name'] for name in species_data['names'] if name['language']['name'] == 'fr'),
            name  # Si la traduction n'existe pas, on garde le nom en anglais
        )

        # Conversion des unités de taille et poids
        height_m = sprite_data['height'] / 10.0
        weight_kg = sprite_data['weight'] / 10.0
        context = {
            'name': french_name,
            'image_url': image_url,
            'height': height_m,
            'weight': weight_kg,
            'base_experience': sprite_data['base_experience'],
        }
        return render(request, 'pokemon_detail.html', context)
    else:
        return render(request, 'pokemon_detail.html', {'error': 'Could not retrieve Pokémon details'})


# Constantes pour la gestion des traductions (actuellement vide)
FRENCH_TO_ENGLISH = {
        'Bulbizarre': 'bulbasaur',
    'Herbizarre': 'ivysaur',
    'Florizarre': 'venusaur',
    'Salamèche': 'charmander',
    'Reptincel': 'charmeleon',
    'Dracaufeu': 'charizard',
    'Carapuce': 'squirtle',
    'Carabaffe': 'wartortle',
    'Tortank': 'blastoise',
    'Chenipan': 'caterpie',
    'Chrysacier': 'metapod',
    'Papilusion': 'butterfree',
    'Aspicot': 'weedle',
    'Coconfort': 'kakuna',
    'Dardargnan': 'beedrill',
    'Roucool': 'pidgey',
    'Roucoups': 'pidgeotto',
    'Roucarnage': 'pidgeot',
    'Rattata': 'rattata',
    'Rattatac': 'raticate',
    'Piafabec': 'spearow',
    'Rapasdepic': 'fearow',
    'Abo': 'ekans',
    'Arbok': 'arbok',
    'Pikachu': 'pikachu',
    'Raichu': 'raichu',
    'Sabelette': 'sandshrew',
    'Sablaireau': 'sandslash',
    'Nidoran♀': 'nidoran-f',
    'Nidorina': 'nidorina',
    'Nidoqueen': 'nidoqueen',
    'Nidoran♂': 'nidoran-m',
    'Nidorino': 'nidorino',
    'Nidoking': 'nidoking',
    'Mélofée': 'clefairy',
    'Mélodelfe': 'clefable',
    'Goupix': 'vulpix',
    'Feunard': 'ninetales',
    'Rondoudou': 'jigglypuff',
    'Grodoudou': 'wigglytuff',
    'Nosferapti': 'zubat',
    'Nosferalto': 'golbat',
    'Mystherbe': 'oddish',
    'Ortide': 'gloom',
    'Rafflesia': 'vileplume',
    'Paras': 'paras',
    'Parasect': 'parasect',
    'Mimitoss': 'venonat',
    'Aéromite': 'venomoth',
    'Taupiqueur': 'diglett',
    'Triopikeur': 'dugtrio',
    'Miaouss': 'meowth',
    'Persian': 'persian',
    'Psykokwak': 'psyduck',
    'Akwakwak': 'golduck',
    'Férosinge': 'mankey',
    'Colossinge': 'primeape',
    'Caninos': 'growlithe',
    'Arcanin': 'arcanine',
    'Ptitard': 'poliwag',
    'Têtarte': 'poliwhirl',
    'Tartard': 'poliwrath',
    'Abra': 'abra',
    'Kadabra': 'kadabra',
    'Alakazam': 'alakazam',
    'Machoc': 'machop',
    'Machopeur': 'machoke',
    'Mackogneur': 'machamp',
    'Chétiflor': 'bellsprout',
    'Boustiflor': 'weepinbell',
    'Empiflor': 'victreebel',
    'Tentacool': 'tentacool',
    'Tentacruel': 'tentacruel',
    'Racaillou': 'geodude',
    'Gravalanch': 'graveler',
    'Grolem': 'golem',
    'Ponyta': 'ponyta',
    'Galopa': 'rapidash',
    'Ramoloss': 'slowpoke',
    'Flagadoss': 'slowbro',
    'Magnéti': 'magnemite',
    'Magnéton': 'magneton',
    'Canarticho': 'farfetchd',
    'Doduo': 'doduo',
    'Dodrio': 'dodrio',
    'Otaria': 'seel',
    'Lamantine': 'dewgong',
    'Tadmorv': 'grimer',
    'Grotadmorv': 'muk',
    'Kokiyas': 'shellder',
    'Crustabri': 'cloyster',
    'Fantominus': 'gastly',
    'Spectrum': 'haunter',
    'Ectoplasma': 'gengar',
    'Onix': 'onix',
    'Soporifik': 'drowzee',
    'Hypnomade': 'hypno',
    'Krabby': 'krabby',
    'Krabboss': 'kingler',
    'Voltorbe': 'voltorb',
    'Électrode': 'electrode',
    'Noeunoeuf': 'exeggcute',
    'Noadkoko': 'exeggutor',
    'Osselait': 'cubone',
    'Ossatueur': 'marowak',
    'Kicklee': 'hitmonlee',
    'Tygnon': 'hitmonchan',
    'Excelangue': 'lickitung',
    'Smogo': 'koffing',
    'Smogogo': 'weezing',
    'Rhinocorne': 'rhyhorn',
    'Rhinoféros': 'rhydon',
    'Leveinard': 'chansey',
    'Saquedeneu': 'tangela',
    'Kangourex': 'kangaskhan',
    'Hypotrempe': 'horsea',
    'Hypocéan': 'seadra',
    'Poissirène': 'goldeen',
    'Poissoroy': 'seaking',
    'Stari': 'staryu',
    'Staross': 'starmie',
    'M. Mime': 'mr-mime',
    'Insécateur': 'scyther',
    'Lippoutou': 'jynx',
    'Élektek': 'electabuzz',
    'Magmar': 'magmar',
    'Scarabrute': 'pinsir',
    'Tauros': 'tauros',
    'Magicarpe': 'magikarp',
    'Léviator': 'gyarados',
    'Lokhlass': 'lapras',
    'Métamorph': 'ditto',
    'Évoli': 'eevee',
    'Aquali': 'vaporeon',
    'Voltali': 'jolteon',
    'Pyroli': 'flareon',
    'Porygon': 'porygon',
    'Amonita': 'omanyte',
    'Amonistar': 'omastar',
    'Kabuto': 'kabuto',
    'Kabutops': 'kabutops',
    'Ptéra': 'aerodactyl',
    'Ronflex': 'snorlax',
    'Artikodin': 'articuno',
    'Électhor': 'zapdos',
    'Sulfura': 'moltres',
    'Minidraco': 'dratini',
    'Draco': 'dragonair',
    'Dracolosse': 'dragonite',
    'Mewtwo': 'mewtwo',
    'Mew': 'mew'

}

# Fonction pour récupérer les données d'un Pokémon
def fetch_pokemon_data(name):
    english_name = FRENCH_TO_ENGLISH.get(name, name.lower())  # Utilise la traduction si elle existe
    url = f"https://pokeapi.co/api/v2/pokemon/{english_name}"
    response = requests.get(url)
    print(f"Fetching data for: {name} (translated: {english_name})")
    if response.status_code == 200:
        data = response.json()
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data.get('stats', [])}
        return {
            'name': data.get('name', 'Unknown').capitalize(),
            'image_url': data.get('sprites', {}).get('front_default', 'https://via.placeholder.com/80'),
            'stats': {
                'hp': stats.get('hp', 0),
                'attack': stats.get('attack', 0),
                'defense': stats.get('defense', 0),
            },
            'types': [t['type']['name'] for t in data.get('types', [])],
        }
    print(f"Failed to fetch data for {name}, status code: {response.status_code}")
    return None


# Vue pour gérer le combat entre le joueur et l'IA
def battle_view(request):
    team_names = request.session.get('team', [])
    if not team_names:
        return render(request, 'battle.html', {'error': "Votre équipe est vide. "})

    # Récupère les données des pokémons du joueur
    player_team = [fetch_pokemon_data(name) for name in team_names if fetch_pokemon_data(name)]
    if not player_team:
        return render(request, 'battle.html', {'error': "Impossible de récupérer les données."})

    # Génère l'équipe de l'IA
    api_url = "https://pokeapi.co/api/v2/pokemon?limit=150"
    response = requests.get(api_url)
    ia_team = []
    if response.status_code == 200:
        pokemons = response.json()['results']
        ia_team = [fetch_pokemon_data(pokemon['name']) for pokemon in random.sample(pokemons, len(player_team))]

    request.session['player_team'] = player_team
    request.session['ia_team'] = ia_team
    request.session['current_player_index'] = 0
    request.session['current_ia_index'] = 0

    # Initialisation du journal de combat
    request.session['battle_log'] = []

    return render(request, 'battle.html', {
        'player_team': player_team,
        'ia_team': ia_team,
    })


# Traitement des tours de combat
def process_turn(request):
    if request.method == "POST":
        action = request.POST.get("action", "attack")
        chosen_index = int(request.POST.get("chosen_pokemon", 0))
        battle_log = request.session.get('battle_log', [])
        player_team = request.session['player_team']
        ia_team = request.session['ia_team']

        player_pokemon = player_team[0]
        ia_pokemon = ia_team[0]

        # Calcul des dégâts
        potential_damage_player = max(1, player_pokemon['stats']['attack'] - ia_pokemon['stats']['defense'] // 2)
        potential_damage_ia = max(1, ia_pokemon['stats']['attack'] - player_pokemon['stats']['defense'] // 2)

        # Gestion du changement de Pokémon
        if action == "change":
            if 0 <= chosen_index < len(player_team):
                if player_team[chosen_index]['stats']['hp'] > 0:
                    battle_log.append(f"Vous changez pour {player_team[chosen_index]['name']}.")
                    player_team.insert(0, player_team.pop(chosen_index))
                    player_pokemon = player_team[0]
                    potential_damage_player = max(1, player_pokemon['stats']['attack'] - ia_pokemon['stats']['defense'] // 2)
                    potential_damage_ia = max(1, ia_pokemon['stats']['attack'] - player_pokemon['stats']['defense'] // 2)

        # Gestion de l'attaque
        if action == "attack":
            if player_pokemon['stats']['hp'] > 0 and ia_pokemon['stats']['hp'] > 0:
                ia_pokemon['stats']['hp'] = max(0, ia_pokemon['stats']['hp'] - potential_damage_player)
                battle_log.append(f"{player_pokemon['name']} inflige {potential_damage_player} dégâts à {ia_pokemon['name']}.")
                if ia_pokemon['stats']['hp'] <= 0:
                    battle_log.append(f"{ia_pokemon['name']} est KO !")
                    ia_team = [p for p in ia_team if p['stats']['hp'] > 0]

            # Attaque de l'IA
            if ia_team and player_pokemon['stats']['hp'] > 0:
                player_pokemon['stats']['hp'] = max(0, player_pokemon['stats']['hp'] - potential_damage_ia)
                battle_log.append(f"{ia_pokemon['name']} inflige {potential_damage_ia} dégâts à {player_pokemon['name']}.")
                if player_pokemon['stats']['hp'] <= 0:
                    battle_log.append(f"{player_pokemon['name']} est KO !")

        # Si l'un des deux a perdu
        if not any(p['stats']['hp'] > 0 for p in player_team):
            request.session['battle_log'] = battle_log
            return render(request, 'result.html', {
                'winner': 'IA',
                'player_team': player_team,
                'ia_team': ia_team,
                'battle_log': battle_log
            })

        if not any(p['stats']['hp'] > 0 for p in ia_team):
            request.session['battle_log'] = battle_log
            return render(request, 'result.html', {
                'winner': 'Joueur',
                'player_team': player_team,
                'ia_team': ia_team,
                'battle_log': battle_log
            })

        request.session['player_team'] = player_team
        request.session['ia_team'] = ia_team
        request.session['battle_log'] = battle_log

        return render(request, 'turn.html', {
            'player_team': player_team,
            'ia_team': ia_team,
            'battle_log': battle_log,
            'player_pokemon': player_pokemon,
            'ia_pokemon': ia_pokemon,
            'potential_damage_player': potential_damage_player,
            'potential_damage_ia': potential_damage_ia,
        })

    return redirect('battle_view')
def ia_turn(player_pokemon, ia_team, battle_log):
    ia_pokemon = ia_team[0]  # L'IA commence avec son premier Pokémon

    # Si le Pokémon de l'IA est KO (ses PV sont inférieurs ou égaux à 0)
    if ia_pokemon['stats']['hp'] <= 0:
        ia_team = [p for p in ia_team if p['stats']['hp'] > 0]  # On filtre l'équipe de l'IA pour garder uniquement les Pokémon vivants
        if ia_team:  # Si l'IA a encore des Pokémon vivants
            ia_pokemon = ia_team[0]  # L'IA choisit son prochain Pokémon disponible (le premier Pokémon vivant)
            battle_log.append(f"L'IA change pour {ia_pokemon['name']}.")  # Enregistre l'action de changement de Pokémon
        return ia_team, ia_pokemon, battle_log  # Retourne l'équipe de l'IA mise à jour, le nouveau Pokémon de l'IA et le journal du combat

    # Si le Pokémon de l'IA a encore des PV, on détermine l'action de l'IA
    action = "attack"  # L'IA commence par l'option d'attaquer par défaut

    # Si les PV du Pokémon de l'IA sont inférieurs à 20 et qu'il a d'autres Pokémon dans l'équipe,
    # il y a une chance de changer de Pokémon
    if ia_pokemon['stats']['hp'] < 20 and len(ia_team) > 1:
        action = "change" if random.random() < 0.5 else "attack"  # L'IA a 50% de chances de changer de Pokémon

    # Si l'action choisie est de changer de Pokémon
    if action == "change":
        # On filtre les Pokémon de l'IA qui sont encore en vie et qui ne sont pas le Pokémon actuel
        available_pokemons = [p for p in ia_team if p['stats']['hp'] > 0 and p != ia_pokemon]
        if available_pokemons:  # Si l'IA a des Pokémon disponibles pour changer
            ia_pokemon = max(available_pokemons, key=lambda p: p['stats']['hp'])  # Choisir le Pokémon avec le plus de PV
            battle_log.append(f"L'IA change pour {ia_pokemon['name']}.")  # Enregistre le changement de Pokémon dans le journal

    # Si l'action choisie est d'attaquer
    elif action == "attack":
        # L'IA inflige des dégâts au Pokémon du joueur. Les dégâts sont calculés par la formule classique Pokémon
        damage = max(1, ia_pokemon['stats']['attack'] - player_pokemon['stats']['defense'] // 2)
        player_pokemon['stats']['hp'] = max(0, player_pokemon['stats']['hp'] - damage)  # On applique les dégâts au Pokémon du joueur
        battle_log.append(f"{ia_pokemon['name']} inflige {damage} dégâts à {player_pokemon['name']}.")  # Enregistre l'attaque dans le journal
        if player_pokemon['stats']['hp'] <= 0:  # Si les PV du Pokémon du joueur sont tombés à 0 ou en dessous
            battle_log.append(f"{player_pokemon['name']} est KO !")  # On annonce que le Pokémon du joueur est KO

    return ia_team, ia_pokemon, battle_log  # Retourne l'équipe de l'IA mise à jour, le Pokémon de l'IA et le journal du combat
