# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 12:21:20 2024

@author: rondo
"""

from streamlit.runtime.scriptrunner import RerunData
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import base64
import plotly.express as px
import pickle
#from streamlit_toggle_switch import st_toggle_switch
import io

#=======================================mise en forme================================================#
# Configuration de la page
st.set_page_config(page_title="DETECTION DE FAUX BILLET", layout="wide")

# Style CSS
st.markdown("""
    <style>
        .title {
            font-size: 2em;
            color: #4CAF50;
            font-weight: bold;
            text-align: center;
        }
        .section-title {
            font-size: 1.5em;
            color: #FF5733;
            margin-top: 10px;
            font-weight: bold;
            text-align: center;
        }
        .search-box input {
            font-size: 1em;
            padding: 8px;
            padding-left: 12px;
            border-radius: 5px;
            border: 1px solid #ddd;
            width: 100%;
        }
       
        .centered-table {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 90%;
        }
       
        .scrollable-table {
            max-height: 400px;
            overflow-y: auto;
            width: 90%;
            margin: auto;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)




# Afficher "Powered by @Big Data" avec une marge négative
st.markdown(
    """
    <style>
    @font-face {
        font-family: 'Bahnschrift Condensed';
        src: url('https://fonts.cdnfonts.com/s/12502/Bahnschrift.ttf') format('truetype');
    }

    .powered-by {
        font-size: 20px;
        color: #000000;  
        text-align: center;
        font-family: 'Bahnschrift Condensed', sans-serif;  
        font-weight: bold;
        margin-top: -30px;
        transition: color 0.6s ease;  
    }
    .powered-by span {
        color: #FFD700;  
        font-size: 22px;
        transition: color 0.3s ease;
    }
    .powered-by:hover {
        color: #000000;
    }
    .powered-by span:hover {
        color: #FFC300;
    }
    </style>
    <div class="powered-by">Powered by <span>@MBA BIG DATA 2</span></div>
    """,
    unsafe_allow_html=True
)


# mettre au centre les tables
st.markdown("""
            <style>
            .scrollable-table {
                max-height: 400px;
                max-width: 100%;
                overflow-x: auto;
                overflow-y: auto;
                white-space: nowrap;
                }
                table {
                    table-layout: auto;
                    width: 100%;
                }
               
            </style>
            """, unsafe_allow_html=True)
           


# Afficher le logo tout en haut à gauche de la page principale
st.markdown("""
    <div style='position: absolute; top: 0; left: 0;'>
        <img src='data:image/png;base64,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'
        alt='logo_ism.jpeg' width='100'>
    </div>
    """, unsafe_allow_html=True)


# Ajouter un espacement entre le logo et le titre
st.markdown("<br><br><br>", unsafe_allow_html=True)

#Charger le model et le scaler
@st.cache_resource
def charger_model_et_scaler():
    model = pickle.load(open("classification_model.pkl", "rb"))
    scaler = pickle.load(open("scaler_2.pkl", "rb"))
    return model, scaler

#rappel du modele
model, scaler = charger_model_et_scaler()


# Créer deux colonnes pour aligner l'image et le texte côte à côte
col1, col2 = st.columns([1, 15])

# Afficher l'image dans la première colonne
with col1:
    st.image("image.png", width=65)

# Afficher le texte dans la deuxième colonne
with col2:
    st.write("### DETECTION DE FAUX BILLET ")
   
# Charger un fichier d'exemple


# Charger le fichier CSV
fichier_csv = "billets_test_1.csv"
df = pd.read_csv(fichier_csv)  # Utiliser pd.read_csv car c'est un fichier CSV

# Convertir le DataFrame en fichier Excel dans un buffer pour le téléchargement
buffer = io.StringIO()
df.to_csv(buffer, index=False)
csv_data = buffer.getvalue()


# Interface Streamlit
with st.expander("📖 Étape 1 : Guide"):
    st.write("""
    Importez un fichier Excel contenant 06 colonnes :  *diagonal,height_left,height_right,margin_low,margin_up,length,id*
    """)

    st.download_button(
        label="📥 Télécharger l'exemple de fichier CSV",
        data=csv_data,
        file_name="billets_test.csv",
        mime="text/csv"
    )

with st.expander("📂 Étape 2 : Charger votre fichier"):
    st.write("""
    Téléversez le fichier Excel.
    """)
    uploaded_file = st.file_uploader("Cliquez ici", type=["csv"])

with st.expander("✅ Résultats attendus"):
    st.write("""
    Obtenez vos predictions: *Prédiction,proba_faux, **proba_vrai*
    """)
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Aperçu des données: ")
        st.dataframe(data, use_container_width=True)
        
        #verifier que les colonnes nécessaires sont présentes
        collonnes_attendues = ["diagonal", "height_left", "height_right", "margin_low", "margin_up", "length"]
        if not all(col in data.columns for col in collonnes_attendues):
            st.error(f"Le fichier doit contenir les colonnes suivantes : {', '.join(collonnes_attendues)}")
        else:
            X=data[collonnes_attendues]
            X_scaled = scaler.transform(X)
            with st.spinner("prédictions..."):
                predictions = model.predict(X_scaled)
                probabilites= model.predict_proba(X_scaled)
                
            #Créer un dataframe pour les résultats
            results_df = pd.DataFrame(
                {
                    "Prédictions":predictions,
                    "Probabilités Faux":probabilites[:,0],
                    "Probabilités Vrai":probabilites[:,1]
                    })
            
            #Afficher les resultats à deux chiffres après la virgule
            results_df["Probabilités Faux"] = results_df["Probabilités Faux"].map(lambda x: f"{x:2f}")
            results_df["Probabilités Vrai"] = results_df["Probabilités Vrai"].map(lambda x: f"{x:2f}")
            
            #Afficher les résultats
            st.write("Résultts des Prédictions : ")
            st.dataframe(results_df, use_container_width=True)
            
            #Histogramme
            prediction_counts = results_df["Prédictions"].replace({0: "Faux billet", 1: "Vrai billet"}).value_counts().reset_index()
            prediction_counts.columns = ["Type de billet",  "Nombre"]
            
            fig = px.bar(prediction_counts,
                         x = "Type de billet", y ="Nombre",
                         title = "Distribution des Prédictions")
            st.plotly_chart(fig, use_container_width= True)

   
# appliquer le dark mode

@st.cache_data(show_spinner=False)
def appliquer_dark_mode(dark_mode):
    if dark_mode:
        st.markdown("""
            <style>
            body, .stApp {
                background-color: #1E1E1E; /* Fond sombre global */
                color: #000000; /* Texte gris clair */
            }
            .stButton>button, .stDownloadButton>button {
                background-color: #444444;
                color: #000000;
            }
            .stDataFrame, .stTable, .stSidebar {
                background-color: #333333;
                color: #000000;
            }
            h1, h2, h3, h4, h5, h6, p, div, label, .section-title {
                color: #B0B0B0;
            }
            .custom-title {
                color: #B0B0B0;
            }
            /* Styles spécifiques pour les sliders */
            .stSlider > div > div {
                color: #B0B0B0;
            }
            .stSlider > div > div > div > div {
                background-color: #FFFF00;
            }
            .powered-by {
                font-size: 20px;
                color: #B0B0B0;
                text-align: center;
                font-family: 'Bahnschrift Condensed', sans-serif;  
                font-weight: bold;
                margin-top: -30px;
                transition: color 0.6s ease;  
            }
            .powered-by span {
                color: #FFD700;  
                font-size: 22px;
                transition: color 0.3s ease;
            }
            .powered-by:hover {
                color: #B0B0B0;
            }
            .powered-by span:hover {
                color: #FFC300;
            }
           
            .stSelectbox, .stSelectbox > div {
                background-color: #333333;
                color: #B0B0B0;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            body, .stApp {
                background-color: #ffffff;
                color: #000000;
            }
            .stButton>button, .stDownloadButton>button {
                background-color: #f0f0f0;
                color: #000000;
            }
            .stDataFrame, .stTable, .stSidebar {
                background-color: #ffffff;
                color: #000000;
            }
            h1, h2, h3, h4, h5, h6, p, div, label, .section-title {
                color: #000000;
            }
            .custom-title {
                color: #000000;
            }
            </style>
        """, unsafe_allow_html=True)
# Footer
st.markdown("""
    </div> <!-- Main content -->
    <div class="footer">
        &copy; 2024 - Créé par Rondouba | Data Science et Machine Learning
    </div>
""", unsafe_allow_html=True)

# un toggle switch
#dark_mode = st_toggle_switch(label="Mode sombre",
#                             key="dark_mode",
#                             default_value=False,
#                             label_after=False)

# mode sombre
#appliquer_dark_mode(dark_mode)