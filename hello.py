from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MultiplyForm(FlaskForm):
    number = DecimalField('Enter a number to multiply by 2:', validators=[DataRequired()])
    submit = SubmitField('Multiply')


# Formulario para buscar un término en Wikipedia
class WikipediaForm(FlaskForm):
    search_term = StringField('Search Wikipedia:', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/multiply', methods=['GET', 'POST'])
def multiply():
    result = None
    form = MultiplyForm()
    if form.validate_on_submit():
        number = form.number.data
        result = number * 2
    return render_template('multiply.html', form=form, result=result)


# Nueva ruta para consultar datos de COVID-19 desde una API
@app.route('/covid', methods=['GET'])
def covid():
    url = 'https://api.api-ninjas.com/v1/covid19?country=mexico'
    api_key = 'cuizZxSDNv6hxR6OQOwO3A==6X6grd9NZVoFijXh'
    headers = {'X-Api-Key': api_key}

    response = requests.get(url, headers=headers)
    confirmed_cases = None
    target_date = '2021-10-27'

    if response.status_code == 200:
        data = response.json()
        if data and 'cases' in data[0]:
            cases = data[0]['cases']
            if target_date in cases:
                confirmed_cases = cases[target_date]['total']
    
    return render_template('covid.html', confirmed_cases=confirmed_cases, target_date=target_date)



# Nueva ruta para buscar información en Wikipedia
@app.route('/wikipedia', methods=['GET', 'POST'])
def wikipedia():
    form = WikipediaForm()
    episode_list = []

    if form.validate_on_submit():
        search_term = form.search_term.data
        # URL fija para la serie Titans según tu ejemplo
        url = "https://en.wikipedia.org/wiki/Titans_(2018_TV_series)"
        page = requests.get(url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            tables = soup.find_all("table", class_="wikiepisodetable")

            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    title_column = row.find("td", class_="summary")
                    if title_column:
                        title = title_column.get_text(strip=True).strip('"')
                        episode_list.append(title)
        else:
            episode_list = ["No episodes found or unable to retrieve information."]

    return render_template('wikipedia.html', form=form, episode_list=episode_list)




if __name__ == '__main__':
    app.run(debug=True)
