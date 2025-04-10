
import streamlit as st
import pandas as pd
import joblib

# Titre de l'application
st.title("Détection de fraude par carte bancaire")

# Explication
st.markdown("""
Cette application utilise un modèle de Machine Learning pour détecter automatiquement les fraudes à partir d'un fichier CSV contenant des transactions.
""")

# Charger le modèle
model = joblib.load("model.pkl")

# Charger un fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Vérification des colonnes
    if 'Class' in data.columns:
        data = data.drop(['Class'], axis=1)

    # Prédictions
    predictions = model.predict(data)
    prediction_proba = model.predict_proba(data)[:, 1]

    # Résultats
    result_df = data.copy()
    result_df['Fraude (1=Oui, 0=Non)'] = predictions
    result_df['Probabilité de fraude'] = prediction_proba

    st.write("### Aperçu des résultats :")
    st.dataframe(result_df.head())

    # Résumé
    total_fraudes = result_df['Fraude (1=Oui, 0=Non)'].sum()
    st.success(f"Nombre total de fraudes détectées : {int(total_fraudes)}")
