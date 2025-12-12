from flask import Flask, render_template, jsonify
from urllib.request import urlopen
import json
from datetime import datetime

app = Flask(__name__)


# ---------------------------
# Page d'accueil
# ---------------------------
@app.route("/")
def hello_world():
    return render_template("hello.html")


# ---------------------------
# Exercice 5 : Page de contact (HTML stylé)
# ---------------------------
@app.route("/contact/")
def contact():
    return render_template("contact.html")


# ---------------------------
# Exercice 3 : API météo Tawarano (JSON)
# ---------------------------
@app.route("/tawarano/")
def meteo():
    # Appel de l'API d'exemple OpenWeatherMap
    response = urlopen(
        "https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx"
    )
    raw_content = response.read()
    json_content = json.loads(raw_content.decode("utf-8"))

    results = []
    # On parcourt la liste des relevés météo
    for list_element in json_content.get("list", []):
        dt_value = list_element.get("dt")  # timestamp
        temp_day_value = (
            list_element.get("main", {}).get("temp") - 273.15
        )  # Kelvin → °C
        results.append({"Jour": dt_value, "temp": temp_day_value})

    # On renvoie un JSON structuré
    return jsonify(results=results)


# ---------------------------
# Exercice 3 bis / ter : Graphique Tawarano (Google Charts)
# ---------------------------
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


# ---------------------------
# Exercice 4 : Histogramme des températures
# ---------------------------
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")


# ---------------------------
# Exercice 6 : API JSON des commits GitHub
# ---------------------------
@app.route("/commits/")
def commits():
    # API publique GitHub du repo original
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = urlopen(url)
    raw_data = response.read()
    commits = json.loads(raw_data.decode("utf-8"))

    results = []

    for commit in commits:
        try:
            # Exemple : "2024-02-11T11:57:27Z"
            date_str = commit["commit"]["author"]["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minute_value = date_obj.minute
            results.append({"date": date_str, "minute": minute_value})
        except Exception:
            # En cas de clé manquante ou autre, on ignore
            continue

    return jsonify(results=results)


# Route bonus de l'énoncé : extraction des minutes d'une date ISO
@app.route("/extract-minutes/<date_string>")
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    minutes = date_object.minute
    return jsonify({"minutes": minutes})


# ---------------------------
# Exercice 6 : Page graphique des commits
# ---------------------------
@app.route("/commits-graph/")
def commits_graph():
    return render_template("commits.html")


if __name__ == "__main__":
    app.run(debug=True)
