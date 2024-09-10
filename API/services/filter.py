import spacy
import pandas as pd
import os


# Load the French language model from spaCy
nlp = spacy.load('fr_core_news_md')

# Define the keywords to search for
mots_cles = ["informatique", "réseaux", "serveur", "matériel informatique", "sécurité informatique", "équipements", "switch", "routeur"]

def analyse_texte(texte, mots_cles):
    doc = nlp(texte.lower())
    for token in doc:
        if token.lemma_ in mots_cles:
            return True
    return False

def filter_files():
    chemin_dossier = "C:/Users/Mselle FAIZOUN/Downloads"
    fichiers_excel = [f for f in os.listdir(chemin_dossier) if f.endswith('.xlsx')]
    fichiers_pertinents = []

    for fichier in fichiers_excel:
        chemin_fichier = os.path.join(chemin_dossier, fichier)
        try:
            df = pd.read_excel(chemin_fichier)
        except Exception as e:
            print(f"Erreur lors de la lecture de {fichier}: {e}")
            continue

        texte_concatene = " ".join(df.astype(str).values.flatten())
        if analyse_texte(texte_concatene, mots_cles):
            fichiers_pertinents.append(fichier)

    print("Fichiers contenant des mots-clés pertinents :")
    for fichier in fichiers_pertinents:
        print(fichier)
            
    return fichiers_pertinents
