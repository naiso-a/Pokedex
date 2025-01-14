from django.core.cache import cache
import requests
from django.shortcuts import render
from .models import Pokemon
def pokedex(request):
    search_query = request.GET.get('search', '').lower()
    pokemons = cache.get('translated_pokemons')

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
                        'image_url': sprite_data.get('sprites', {}).get('front_default', None)
                    })
            cache.set('translated_pokemons', translated_pokemons, timeout=3600)
        else:
            translated_pokemons = []
    else:
        translated_pokemons = pokemons

    # Filtrer les résultats
    if search_query:
        translated_pokemons = [
            p for p in translated_pokemons if search_query in p['name'].lower()
        ]

    return render(request, 'pokedex.html', {'pokemons': translated_pokemons})