import plotly.express as px
import dash
from dash import dcc, html 
from dash.dependencies import Input, Output
import pandas as pd

# Chargement des données à partir du fichier CSV
natural_disaster_df = pd.read_csv('natural_disaster.csv')

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Définition de la mise en page initiale de l'application
app.layout = html.Div(children=[
    # Titre
    html.H1(children='Histogramme des décès dus aux catastrophes naturelles',
            style={'textAlign': 'center', 'color': '#7FDBFF'}),
    
    # RangeSlider pour sélectionner la plage d'années
    dcc.RangeSlider(
        id='year-slider',
        min=natural_disaster_df['Year'].min(),
        max=natural_disaster_df['Year'].max(),
        value=[natural_disaster_df['Year'].min(), natural_disaster_df['Year'].max()],
        marks={str(year): str(year) for year in natural_disaster_df['Year'].unique() if year % 10 == 0},
        step=1,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    
    # Histogrammes
    dcc.Graph(id='graph1'),
    dcc.Graph(id='graph2'),
    
    # Description
    html.Div(children=f'''
        Les histogrammes représentent la distribution du nombre total de décès 
        dus aux catastrophes naturelles.
    ''')
])

# Rappel pour mettre à jour les histogrammes en fonction de la sélection de l'année
@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure')],
    [Input('year-slider', 'value')]
)
def update_histogram(selected_years):
    filtered_df = natural_disaster_df[(natural_disaster_df['Year'] >= selected_years[0]) & 
                                      (natural_disaster_df['Year'] <= selected_years[1])]
    
    fig1 = px.histogram(filtered_df, x="Total Deaths",
                        color="Disaster Subgroup",
                        title="Histogramme global du nombre total de décès dus aux catastrophes naturelles",
                        nbins=50,
                        log_y=True,
                        hover_data=["Disaster Subgroup"])
    
    fig2 = px.histogram(filtered_df[(filtered_df["Total Deaths"] >= 0) & 
                                    (filtered_df["Total Deaths"] <= 10000)],
                        x="Total Deaths",
                        color="Disaster Subgroup",
                        title="Histogramme des décès (0 à 10,000) dus aux catastrophes naturelles",
                        nbins=100,
                        log_y=True,
                        hover_data=["Disaster Subgroup"])
    
    return fig1, fig2

# Démarrage du serveur Dash
if __name__ == '__main__':
    app.run_server(debug=True)
