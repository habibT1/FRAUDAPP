
# App.py corrigé - Application de détection de fraude avec Streamlit

import streamlit as st
import pandas as pd
import joblib

# Titre de l'application
st.title("Détection de Fraude par Carte Bancaire")

# Charger le modèle
model = joblib.load("Modèle.pkl")

# Charger les noms de colonnes utilisés à l'entraînement
try:
    expected_features = model.feature_names_in_
except AttributeError:
    with open("features.txt") as f:
        expected_features = [line.strip() for line in f.readlines()]

# Uploader le fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV contenant les transactions", type=["csv"])

if uploaded_file is not None:
    try:
        # Lire le fichier
        data = pd.read_csv(uploaded_file)

        # Afficher les données brutes
        st.subheader("Aperçu des données")
        st.write(data.head())

        # Vérifier et filtrer les colonnes attendues
        missing_cols = [col for col in expected_features if col not in data.columns]
        if missing_cols:
            st.error(f"Les colonnes suivantes sont manquantes dans le fichier : {missing_cols}")
        else:
            data = data[expected_features]  # S'assurer de l'ordre et de la présence des colonnes

            # Prédiction
            predictions = model.predict(data)

            # Afficher les résultats
            st.subheader("Résultats de la détection")
            data['Fraude_prédite'] = predictions
            st.write(data)

            # Téléchargement des résultats
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger les résultats",
                data=csv,
                file_name='resultats_fraude.csv',
                mime='text/csv'
            )
    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier : {e}")
else:
    st.info("Veuillez téléverser un fichier CSV pour commencer.")
