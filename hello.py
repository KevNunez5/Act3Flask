from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
import requests
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

# Variables globales para el conteo de puntos y rounds
MAX_ROUNDS = 11
app.config['PERROS'] = 0
app.config['GATOS'] = 0
app.config['CURRENT_ROUND'] = 1


# Funciones para obtener URLs de imágenes y nombres de razas
def obtener_gato_random():
    breeds_url = "https://api.thecatapi.com/v1/breeds"
    breeds_response = requests.get(breeds_url)

    if breeds_response.status_code == 200:
        breeds = breeds_response.json()
        
        if breeds:
            random_breed = random.choice(breeds)
            breed_name = random_breed['name']
            image_url = f"https://api.thecatapi.com/v1/images/search?breed_ids={random_breed['id']}"
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                image_data = image_response.json()
                if image_data:
                    return breed_name, image_data[0]['url']
                else:
                    return breed_name, None
            else:
                return breed_name, None
    return None, None


def obtener_perro_random():
    breeds_url = "https://api.thedogapi.com/v1/breeds"
    breeds_response = requests.get(breeds_url)

    if breeds_response.status_code == 200:
        breeds = breeds_response.json()

        if breeds:
            random_breed = random.choice(breeds)
            breed_name = random_breed['name']
            image_url = f"https://api.thedogapi.com/v1/images/search?breed_ids={random_breed['id']}"
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                image_data = image_response.json()
                if image_data:
                    return breed_name, image_data[0]['url']
                else:
                    return breed_name, None
            else:
                return breed_name, None
    return None, None


# Pantalla de inicio del juego
@app.route('/')
def index():
    # Reinicia el juego cuando se visita la página de inicio
    app.config['PERROS'] = 0
    app.config['GATOS'] = 0
    app.config['CURRENT_ROUND'] = 1
    return render_template('index.html')


# Pantalla de rounds donde se muestran las imágenes y se elige entre perro o gato
@app.route('/rounds', methods=['GET', 'POST'])
def rounds():
    if app.config['CURRENT_ROUND'] > MAX_ROUNDS:
        return redirect(url_for('victory'))

    # Obtener URLs e información de razas
    perro_raza, perro_url = obtener_perro_random()
    gato_raza, gato_url = obtener_gato_random()

    if request.method == 'POST':
        # Sumar puntos según la imagen seleccionada
        if 'perro' in request.form:
            app.config['PERROS'] += 1
        elif 'gato' in request.form:
            app.config['GATOS'] += 1

        # Avanza al siguiente round
        app.config['CURRENT_ROUND'] += 1

        if app.config['CURRENT_ROUND'] > MAX_ROUNDS:
            return redirect(url_for('victory'))
    
    return render_template('rounds.html', perro_url=perro_url, gato_url=gato_url, round=app.config['CURRENT_ROUND'], perro_raza=perro_raza, gato_raza=gato_raza)


# Pantalla final donde se muestra el equipo ganador
@app.route('/victory')
def victory():
    if app.config['PERROS'] > app.config['GATOS']:
        winner = "Perros"
    elif app.config['GATOS'] > app.config['PERROS']:
        winner = "Gatos"
    else:
        winner = "Empate"

    return render_template('victoria.html', winner=winner, perros=app.config['PERROS'], gatos=app.config['GATOS'])


if __name__ == '__main__':
    app.run(debug=True)
