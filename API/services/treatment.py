import pandas as pd
import os,spacy
from models.markets import PlanDePassation, Marche
from datetime import datetime

nlp = spacy.load('fr_core_news_md')

file_path= "C:/Users/Mselle FAIZOUN/Downloads"

# Fonction pour traiter un fichier Excel et insérer les données dans la base de données
def traiter_fichier_excel_et_inserer_db(file_path, session):
    try:
        df = pd.read_excel(file_path)
        df = df.fillna('')  # Handle missing values
        
        # Extraction des informations générales du plan de passation
        nom_autorite_contractante = df.iloc[1, 0]
        plan_id = df.iloc[1, 0]  # Identifiant unique du plan, pourrait être le nom de l'autorité
        
        if isinstance(plan_id, str):
            plan_id = plan_id.replace(" ", "_").lower()
        else:
            # Générer un plan_id par défaut basé sur le nom de fichier
            plan_id = os.path.splitext(os.path.basename(file_path))[0].replace(" ", "_").lower()
            print(f"Avertissement : plan_id généré automatiquement pour {file_path}")

        info_plan_passation = {
            "nom_autorite_contractante": nom_autorite_contractante,
            "periode_couverte": df.iloc[4, 3],
            "plan_id": plan_id
        }

        # Vérification si le plan de passation existe déjà
        plan_exist = session.query(PlanDePassation).filter_by(plan_id=info_plan_passation['plan_id']).first()
        if not plan_exist:
            nouveau_plan = PlanDePassation(
                plan_id=info_plan_passation['plan_id'],
                nom_autorite_contractante=info_plan_passation['nom_autorite_contractante'],
                periode_couverte=info_plan_passation['periode_couverte']
            )
            session.add(nouveau_plan)
            session.commit()

        # Renommer les colonnes du DataFrame
        df.columns = [
            'N', 'Réf N°', 'Description', 'Type de marché', 'Mode de Passation', 'Montant Estimatif',
            'Source de financement', 'Ligne d\'imputation', 'Organe de contrôle', 'Autorisation d\'engagement',
            'Date de réception du Dossier', 'Date de réception de l\'avis', 'Date de l\'avis',
            'Date de réception du dossier corrigé', 'Date d\'autorisation du lancement', 'Date de publication de l\'avis',
            'Date d\'ouverture des plis', 'Date de réception des rapports', 'Date de réception de l\'avis 2',
            'Date de réception de l\'avis 3', 'Date d\'examen juridique', 'Date d\'approbation du contrat',
            'Date de notification du contrat'
        ]
        
        # Extraire les données des marchés
        df_marche = df.loc[9:, ['N', 'Réf N°', 'Description', 'Type de marché', 'Montant Estimatif', 'Date d\'approbation du contrat']].copy()

# Convertir la colonne 'Date d'approbation du contrat' en type datetime
        df_marche['Date d\'approbation du contrat'] = pd.to_datetime(df_marche['Date d\'approbation du contrat'], errors='coerce')

# Filtrer les lignes où 'Montant Estimatif' est vide ou non numérique
        df_marche = df_marche[pd.to_numeric(df_marche['Montant Estimatif'], errors='coerce').notnull()]

# Convertir 'Montant Estimatif' en float
        df_marche['Montant Estimatif'] = df_marche['Montant Estimatif'].astype(float)

        # Insert data into database
        for index, row in df_marche.iterrows():
            print(f"Insertion de la ligne {index} : {row.to_dict()}")
            statut = "passé" if row['Date d\'approbation du contrat'] <= datetime.now() else "à venir"
            nouveau_marche = Marche(
                plan_id=plan_id,
                n=row['N'],
                reference=row['Réf N°'],
                description=row['Description'],
                type_marche=row['Type de marché'],
                montant_fcfa=row['Montant Estimatif'],
                date_approbation_marche=row['Date d\'approbation du contrat'],
                statut=statut
            )
            session.add(nouveau_marche)
            session.commit()

    
    except Exception as e:
        print(f"Erreur lors du traitement du fichier {file_path}: {e}")
        session.rollback()
    finally:
        session.close()

