from django.core.cache import cache
import requests
from django.shortcuts import render
from .models import Pokemon

def pokedex(request):
    pokemons = cache.get('translated_pokemons')
    if not pokemons:
        api_url = "https://pokeapi.co/api/v2/pokemon?limit=150"
        response = requests.get(api_url)
        if response.status_code == 200:
            pokemons = response.json()['results']
            translated_pokemons = []

            for pokemon in pokemons:
                species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon['name']}"
                sprite_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon['name']}"
                species_response = requests.get(species_url)
                sprite_response = requests.get(sprite_url)
                if species_response.status_code == 200:
                    species_data = species_response.json()
                    sprite_data = sprite_response.json()
                    image_url = sprite_data.get('sprites', {}).get('front_default', None)
                    french_name = next(
                        (name['name'] for name in species_data['names'] if name['language']['name'] == 'fr'),
                        pokemon['name']
                    )
                    translated_pokemons.append({
                        'name': french_name,
                        'english_name': pokemon['name'],
                        'url': pokemon['url'],
                        'image_url': image_url 
                    })
            cache.set('translated_pokemons', translated_pokemons, timeout=3600)
        else:
            translated_pokemons = []
    else:
        translated_pokemons = pokemons

    context = {
        'pokemons': translated_pokemons,
    }
    return render(request, 'pokedex.html', context)

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
        
        height_m = sprite_data['height'] / 10.0  # Conversion de décimètres en mètres
        weight_kg = sprite_data['weight'] / 10.0  # Conversion de hectogrammes en kilogrammes

        context = {
            'name': french_name,
            'image_url': image_url,
            'height': height_m,
            'weight': weight_kg,
            'base_experience': sprite_data['base_experience'],
            # Ajouter d'autres détails ici si nécessaire
        }
        return render(request, 'pokemon_detail.html', context)
    else:
        return render(request, 'pokemon_detail.html', {'error': 'Could not retrieve Pokémon details'})
