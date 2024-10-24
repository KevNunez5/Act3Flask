from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

# Variables globales para el conteo de puntos y rounds
MAX_ROUNDS = 11
app.config['PERROS'] = 0
app.config['GATOS'] = 0
app.config['CURRENT_ROUND'] = 1

# Función que obtiene URLs de imágenes de perros y gatos (debes reemplazar esto con tu propia función)
def obtener_urls_imagenes():
    perro_url = "https://example.com/dog.jpg"  # Simulación, reemplaza con función real
    gato_url = "https://example.com/cat.jpg"   # Simulación, reemplaza con función real
    return perro_url, gato_url


# Pantalla de inicio del juego
@app.route('/')
def index():
    # Reinicia el juego cuando se visita la página de inicio
    app.config['PERROS'] = 0
    app.config['GATOS'] = 0
    app.config['CURRENT_ROUND'] = 1
    return render_template('inicio.html')


# Pantalla de rounds donde se muestran las imágenes y se elige entre perro o gato
@app.route('/rounds', methods=['GET', 'POST'])
def rounds():
    if app.config['CURRENT_ROUND'] > MAX_ROUNDS:
        return redirect(url_for('victory'))

    perro_url, gato_url = obtener_urls_imagenes()

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
    
    return render_template('rounds.html', perro_url=perro_url, gato_url=gato_url, round=app.config['CURRENT_ROUND'])


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
