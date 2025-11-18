from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
LANGS = ["fr", "en", "es", "de", "it"]

# Base de données simple des légendes (pour l’API)
LEGENDS = [
    {
        "id": 1,
        "title": "Aubépin la fille femme",
        "country": "Maroc",
        "lang": "fr",
        "content": "C’est une longue aventure..."
    },
    {
        "id": 2,
        "title": "La Licorne du Val",
        "country": "France",
        "lang": "fr",
        "content": "On raconte qu’une licorne..."
    },
]

# Ancienne liste utilisée par la page “Grimoire”
legendes = [
    "Légende 1 : Dans les ombres des montagnes anciennes...",
    "Légende 2 : Là où les étoiles tombent en poussière...",
    "Légende 3 : Au seuil des royaumes brisés...",
    "Légende 4 : Quand le vent porte les voix disparues...",
    "Légende 5 : Sous la lune d’obsidienne..."
]

# Commentaires du grimoire
commentaires = []

# --------------------------------------------------
# ROUTES MULTILINGUES
# --------------------------------------------------
def render_page(page_name):
    lang = request.args.get("lang", "fr")
    if lang not in LANGS:
        lang = "fr"
    return render_template(f"{page_name}_{lang}.html", lang=lang)

@app.route("/")
def accueil():
    return render_page("accueil")

@app.route("/apropos")
def apropos():
    return render_page("apropos")

@app.route("/dons")
def dons():
    return render_page("dons")

@app.route("/jeddi")
def jeddi():
    return render_page("jeddi")

@app.route("/galerie")
def galerie():
    return render_page("galerie")


# --------------------------------------------------
# PAGE GRIMOIRE AVEC PAGINATION
# --------------------------------------------------
@app.route("/grimoire")
def grimoire():
    lang = request.args.get("lang", "fr")
    page = int(request.args.get("page", 1))

    # Sélection du texte
    index = page - 1
    texte = legendes[index]

    # Pagination
    next_page = page + 1 if page < len(legendes) else None
    prev_page = page - 1 if page > 1 else None

    return render_template(
        "grimoire.html",
        lang=lang,
        texte=texte,
        page=page,
        next_page=next_page,
        prev_page=prev_page,
        commentaires=commentaires
    )


# --------------------------------------------------
# COMMENTAIRES DU GRIMOIRE
# --------------------------------------------------
@app.route("/commentaires", methods=["POST"])
def commentaires_route():
    commentaire = request.form.get("commentaire")    
    if commentaire:
        commentaires.append(commentaire)
    return redirect(url_for("grimoire"))


# --------------------------------------------------
# API JSON (PAYS, ALPHABET, etc.)
# --------------------------------------------------
@app.route("/api/legends")
def api_legends():
    lang = request.args.get("lang", "fr")
    country = request.args.get("country")
    alpha = request.args.get("alpha")

    data = LEGENDS

    # Filtre par langue
    if lang:
        data = [l for l in data if l["lang"] == lang]

    # Filtre par pays
    if country:
        data = [l for l in data if l["country"].lower() == country.lower()]

    # Filtre alphabétique
    if alpha:
        data = [l for l in data if l["title"].lower().startswith(alpha.lower())]

    return jsonify(data)
