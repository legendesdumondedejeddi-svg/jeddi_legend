from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# -----------------------------
# CONTENU
# -----------------------------
legendes = [
    "Légende 1 : Dans les ombres des montagnes anciennes...",
    "Légende 2 : Là où les étoiles tombent en poussière...",
    "Légende 3 : Au seuil des royaumes brisés...",
    "Légende 4 : Quand le vent porte les voix disparues...",
    "Légende 5 : Sous la lune d’obsidienne..."
]

commentaires = []

# -----------------------------
# ROUTES PRINCIPALES
# -----------------------------
@app.route("/")
def accueil():
    lang = request.args.get("lang", "fr")
    template = f"accueil_{lang}.html"
    return render_template(template, lang=lang)

@app.route("/apropos")
def apropos():
    lang = request.args.get("lang", "fr")
    template = f"apropos_{lang}.html"
    return render_template(template, lang=lang)

@app.route("/dons")
def dons():
    lang = request.args.get("lang", "fr")
    template = f"dons_{lang}.html"
    return render_template(template, lang=lang)

@app.route("/jeddi")
def jeddi():
    lang = request.args.get("lang", "fr")
    template = f"jeddi_{lang}.html"
    return render_template(template, lang=lang)

# -----------------------------
# GRIMOIRE + PAGINATION
# -----------------------------
@app.route("/grimoire")
def grimoire():
    lang = request.args.get("lang", "fr")
    page = int(request.args.get("page", 1))

    index = page - 1
    texte = legendes[index]

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

@app.route("/commentaires", methods=["POST"])
def commentaires_route():
    commentaire = request.form.get("commentaire")
    if commentaire:
        commentaires.append(commentaire)
    return redirect(url_for('grimoire'))
