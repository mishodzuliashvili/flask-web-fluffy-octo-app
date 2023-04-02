from flask import Flask, render_template, request

from exceptions import GitHubApiError
from api import repos_with_most_stars

app = Flask(__name__)

available_languages = ["Python", "JavaScript", "Ruby", "Java"]


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        selected_languages = available_languages
    elif request.method == 'POST':
        selected_languages = request.form.getlist("languages")

    results = repos_with_most_stars(selected_languages)
    return render_template(
        'index.html',
        selected_languages=selected_languages,
        available_languages=available_languages,
        results=results
    )

# $env:FLASK_APP='hello.py';$env:FLASK_DEBUG='1';$env:TEMPLATES_AUTO_RELOAD='1'; flask run


@app.errorhandler(GitHubApiError)
def handle_api_error(error):
    return render_template('error.html', message=error)
