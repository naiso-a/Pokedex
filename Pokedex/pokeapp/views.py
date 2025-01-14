from django.core.cache import cache
import requests
from django.shortcuts import render, redirect
from .models import Pokemon

def pokedex(request):
    search_query = request.GET.get('search', '').lower()
    pokemons = cache.get('translated_pokemons')
    team = request.session.get('team', [])

    if not pokemons:
        api_url = "https://pokeapi.co/api/v2/pokemon?limit=150"
        response = requests.get(api_url)
        if response.status_code == 200:
            pokemons = response.json()['results']
            translated_pokemons = []

            for pokemon in pokemons:
                name = pokemon['name']
                species_url = f"https://pokeapi.co/api/v2/pokemon-species/{name}"
                sprite_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
                species_response = requests.get(species_url)
                sprite_response = requests.get(sprite_url)

                if species_response.status_code == 200 and sprite_response.status_code == 200:
                    species_data = species_response.json()
                    sprite_data = sprite_response.json()
                    french_name = next(
                        (n['name'] for n in species_data['names'] if n['language']['name'] == 'fr'),
                        name
                    )
                    translated_pokemons.append({
                        'name': french_name,
                        'image_url': sprite_data.get('sprites', {}).get('front_default', None),
                        'english_name': pokemon['name'],
                    })
            cache.set('translated_pokemons', translated_pokemons, timeout=3600)
        else:
            translated_pokemons = []
    else:
        translated_pokemons = pokemons


    for pokemon in translated_pokemons:
        pokemon['in_team'] = pokemon['name'] in team


    if 'add' in request.GET:
        pokemon_name = request.GET.get('add')
        if pokemon_name not in team and len(team) < 6:
            team.append(pokemon_name)
        request.session['team'] = team


    if 'remove' in request.GET:
        pokemon_name = request.GET.get('remove')
        if pokemon_name in team:
            team.remove(pokemon_name)
        request.session['team'] = team


    if search_query:
        translated_pokemons = [
            p for p in translated_pokemons if search_query in p['name'].lower()
        ]

    return render(request, 'pokedex.html', {
        'pokemons': translated_pokemons,
        'team': team,
    })


def team_view(request):
    # Supprimer un Pokémon spécifique
    remove_pokemon = request.GET.get('remove_pokemon')
    if remove_pokemon:
        team = request.session.get('team', [])
        if remove_pokemon in team:
            team.remove(remove_pokemon)
            request.session['team'] = team
        return redirect('team_view')  # Redirige après suppression

    # Charger les données de l'équipe
    pokemons = cache.get('translated_pokemons', [])
    team_names = request.session.get('team', [])
    team = [pokemon for pokemon in pokemons if pokemon['name'] in team_names]

    return render(request, 'team.html', {'team': team})

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
            name
        )
        
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