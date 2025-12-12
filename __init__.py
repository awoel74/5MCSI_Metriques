from flask import Flask, render_template, jsonify
from urllib.request import urlopen
import json

app = Flask(__name__)

# Route principale : page d'accueil
@app.route("/")
def hello_world():
    return render_template("hello.html")


# Exercice 2 : route /contact/
@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"


# Exercice 3 : API /tawarano/ qui retourne les dates + températures
@app.route("/tawarano/")
def meteo():
    response = urlopen("https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx")
    raw_content = response.read()
    json_content = json.loads(raw_content.decode("utf-8"))

    results = []
    for list_element in json_content.get("list", []):
        dt_value = list_element.get("dt")  # timestamp
        temp_day_value = list_element.get("main", {}).get("temp") - 273.15  # Kelvin → °C
        results.append({"Jour": dt_value, "temp": temp_day_value})

    return jsonify(results=results)


# Exercice 3 bis & 3 ter : route /rapport/ qui affiche le graphique
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

