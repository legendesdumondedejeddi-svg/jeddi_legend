from flask import Flask, render_template, request, redirect, flash
import os

app = Flask(__name__)
app.secret_key = "JeddiSecretKey987"
ADMIN_PASSWORD = "1997.Monde-1958-Jeddi.1998"
LANGS = ["fr", "en", "es", "de", "it"]

SAVE_FOLDER = "legendes"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def load_legend(lang):
    filepath = os.path.join(SAVE_FOLDER, f"legende_{lang}.txt")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_legend(lang, text):
    filepath = os.path.join(SAVE_FOLDER, f"legende_{lang}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

@app.route("/")
def index():
    return redirect("/fr/accueil")

PAGES = ["accueil", "jeddi", "about", "galerie", "legendes", "don"]

for lang in LANGS:
    for page in PAGES:
        route = f"/{lang}/{page}"
        def make_page_route(p=page, l=lang):
            def route_func():
                return render_template(f"{p}_{l}.html", legend_text=load_legend(l))
            return route_func
        app.add_url_rule(route, f"{page}_{lang}", make_page_route())

@app.route("/<lang>/legendes", methods=["GET", "POST"])
def legendes(lang):
    if lang not in LANGS:
        return redirect("/fr/legendes")
    legend_text = load_legend(lang)
    if request.method == "POST":
        text = request.form.get("legend_text", "").strip()
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            save_legend(lang, text)
            flash("✅ Légende enregistrée avec succès.")
            legend_text = text
        else:
            flash("❌ Mot de passe incorrect.")
    return render_template(f"legendes_{lang}.html", legend_text=legend_text)

if __name__ == "__main__":
    app.run(debug=True)
