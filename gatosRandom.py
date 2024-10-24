import requests
import random

# Obtener la lista de razas
breeds_url = "https://api.thecatapi.com/v1/breeds"
breeds_response = requests.get(breeds_url)

if breeds_response.status_code == 200:
    breeds = breeds_response.json()
    
    # Elegir una raza aleatoria
    random_breed = random.choice(breeds)
    breed_name = random_breed['name']
    
    # Obtener una imagen para la raza aleatoria
    image_url = f"https://api.thecatapi.com/v1/images/search?breed_ids={random_breed['id']}"
    image_response = requests.get(image_url)
    
    if image_response.status_code == 200:
        image_data = image_response.json()
        if image_data:  # Verifica si se devolvió una imagen
            image_url = image_data[0]['url']
            print(f"Raza aleatoria: {breed_name} - Imagen: {image_url}")
        else:
            print(f"Raza: {breed_name} - Sin imagen disponible")
    else:
        print(f"Error al obtener imagen para {breed_name}: {image_response.status_code}")
else:
    print(f"Error al obtener razas: {breeds_response.status_code}")
