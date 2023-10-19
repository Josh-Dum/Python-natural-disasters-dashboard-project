# dash-01.py

#
# Imports
#

# Importation des bibliothèques nécessaires pour la visualisation et la création du dashboard
import plotly.express as px
import dash
from dash import dcc, html 
import pandas as pd


#
# Data
#

# Chargement des données à partir du fichier CSV
natural_disaster_df = pd.read_csv('natural_disaster.csv')

#
# Main
#

# Ce bloc garantit que le code ci-dessous n'est exécuté que lorsque ce script est lancé directement
if __name__ == '__main__':

    # Initialisation de l'application Dash
    app = dash.Dash(__name__)

    # Création du premier histogramme en utilisant plotly express
    fig1 = px.histogram(natural_disaster_df, x="Total Deaths",
                   color="Disaster Subgroup",
                   title="Histogramme global du nombre total de décès dus aux catastrophes naturelles",
                   nbins=50,  # Utilisation de 50 intervalles pour l'histogramme
                   log_y=True,
                   hover_data=["Disaster Subgroup"]
                   )

    # Filtrage des données pour inclure uniquement les décès entre 0 et 100,000
    filtered_data_for_fig2 = natural_disaster_df[(natural_disaster_df["Total Deaths"] >= 0) & 
                                        (natural_disaster_df["Total Deaths"] <= 10000)]


    # Création du second histogramme avec les données filtrées
    fig2 = px.histogram(filtered_data_for_fig2, x="Total Deaths",
                       color="Disaster Subgroup",
                       title="Histogramme des décès (0 à 10,000) dus aux catastrophes naturelles",
                       nbins=100,
                       log_y=True,
                       hover_data=["Disaster Subgroup"]
                       )

    # Structure de la mise en page du tableau de bord
    app.layout = html.Div(children=[
        # Ajout d'un titre au tableau de bord pour le premier histogramme
        html.H1(children='Histogramme des décès dus aux catastrophes naturelles',
                style={'textAlign': 'center', 'color': '#7FDBFF'}),

        # Intégration du premier histogramme dans le dashboard
        dcc.Graph(
            id='graph1',
            figure=fig1
        ),

        # Ajout d'un titre pour le second histogramme
        html.H1(children='Histogramme des décès (0 à 100,000) dus aux catastrophes naturelles',
                style={'textAlign': 'center', 'color': '#7FDBFF'}),

        # Intégration du second histogramme dans le dashboard
        dcc.Graph(
            id='graph2',
            figure=fig2
        ),

        # Description textuelle pour fournir des informations complémentaires sur l'histogramme
        html.Div(children=f'''
            Les histogrammes représentent la distribution du nombre total de décès 
            dus aux catastrophes naturelles.
        '''),
    ])

    # Démarrage du serveur Dash
    app.run_server(debug=True)
