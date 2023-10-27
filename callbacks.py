import folium
import plotly_express as px

from dash import dcc, html
from dash.dependencies import Input, Output
from config import *
from main import app

@app.callback(
    Output('content', 'children'),
    [Input('tabs', 'value')]
)
def update_content(tab):
    if tab == 'home':
        return html.Div([
            html.H3("Bienvenue sur le Dashboard"),
            html.P("Veuillez sélectionner un onglet pour afficher son contenu.")
        ])
    elif tab == 'map':
        return generate_map_content()
    elif tab == 'histogram':
        return generate_histogram_content()
    elif tab == 'graph3':
        return generate_graph3_content()
    elif tab == 'graph4':
        return generate_graph4_content()
    # Définition de la fonction de mise à jour en réponse à la sélection de l'utilisateur
def generate_map_content():
    # Votre code pour générer la carte
    return html.Div(children=[
        html.H1(children=f'Carte des catastrophes naturelles'),
        dcc.RangeSlider(id='annees',
                        marks={str(year): str(year) for year in annees if year %10 == 0},
                        min=min(annees),
                        max=max(annees),
                        value=[max(annees)-1, max(annees)],
                        step=1,
                        tooltip={"placement":"bottom","always_visible":True}),
        html.Div(id='map_annee')
    ])

@app.callback(
    Output('map_annee', 'children'),
    [Input('annees', 'value')]
)
def update_map(year_range):
    coord = (48.8398094, 2.5840685) # centré sur l'Esiee
    carte = folium.Map(location = coord, tiles='Stamen Terrain', zoom_start=3)

    debut , fin = year_range
    
    
    feature_groups = {}
    for disaster_type in marqueur_type_de_catastrophe.keys():
        feature_groups[disaster_type] = folium.FeatureGroup(name=disaster_type)

    df_catastrophe_location_selected = df_catastrophe_location[(df_catastrophe_location['Year'] >= debut) & (df_catastrophe_location['Year'] <= fin)]

    for location, latitude, longitude,type_de_catastrophe in zip(df_catastrophe_location_selected['Location'], 
                                                                 df_catastrophe_location_selected['Latitude'], 
                                                                 df_catastrophe_location_selected['Longitude'],
                                                                 df_catastrophe_location_selected['Disaster Type']):
        
        
        coords = [latitude, longitude]

        if type_de_catastrophe in marqueur_type_de_catastrophe:

            icon_color = marqueur_type_de_catastrophe[type_de_catastrophe]['color']
            icon_type = marqueur_type_de_catastrophe[type_de_catastrophe]['icon']
            icon = folium.Icon(color=icon_color, icon=icon_type)
            marker = folium.Marker(location=coords, popup=location, icon=icon)
            marker.add_to(feature_groups[type_de_catastrophe])

    # Ajouter chaque FeatureGroup à la carte
    for fg in feature_groups.values():
        fg.add_to(carte)

    # Ajouter un contrôle pour afficher/masquer chaque FeatureGroup
    folium.map.LayerControl().add_to(carte)

    legend_html = """
    <div style="position: fixed; 
    bottom: 50px; left: 50px; width: 250px; height: auto; 
    border:2px solid grey; z-index:9999; font-size:14px; background-color: white; padding: 10px;">
    &nbsp; <b>Legend</b> <br>
    """

    for catastrophe, attributes in marqueur_type_de_catastrophe.items():
        color = attributes['color']
        icon = attributes['icon'].replace('-sign', '') 
        legend_html += f'&nbsp; <i class="fa fa-map-marker" style="color:{color}"></i>&nbsp; <i class="fa fa-{icon}"></i>&nbsp; {catastrophe} <br>'
        #legend_html += f'&nbsp; <span style="background-color: {color}; display: inline-block; width: 10px; height: 10px;"></span> &nbsp; <i class="fa fa-{icon}"></i>&nbsp; {catastrophe} <br>'

    legend_html += '</div>'
    carte.get_root().html.add_child(folium.Element(legend_html))


    carte.save('map.html')


    return html.Iframe(srcDoc=open('map.html', 'r', encoding='utf-8').read(), width='100%', height='600px')
        
def generate_histogram_content():
    # Votre code pour générer l'histogramme
    return html.Div(children=[
    # Titre
    html.H1(children='Histogramme des décès dus aux catastrophes naturelles',
            style={'textAlign': 'center', 'color': '#7FDBFF'}),
    
    # RangeSlider pour sélectionner la plage d'années
    dcc.RangeSlider(
        id='year-slider',
        min=min(annees),
        max= max(annees),
        value=[min(annees),max(annees)],
        marks={str(year): str(year) for year in annees if year % 10 == 0},
        step=1,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    
    # Histogrammes
    dcc.Graph(id='graph1'),
    dcc.Graph(id='graph2'),
    dcc.Graph(id='graph3'),
    dcc.Graph(id='graph4'),  # Graphique 2D ajouté
    
    # Description
    html.Div(children=f'''
        Les histogrammes représentent la distribution du nombre total de décès 
        dus aux catastrophes naturelles.
    ''')
])

# Rappel pour mettre à jour les histogrammes en fonction de la sélection de l'année
@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure'),
     Output('graph3', 'figure'),
     Output('graph4', 'figure')],  # Graphique 2D ajouté
    [Input('year-slider', 'value')]
)
def update_histogram(selected_years):
    filtered_df = natural_disaster_df[(natural_disaster_df['Year'] >= selected_years[0]) & 
                                      (natural_disaster_df['Year'] <= selected_years[1])]
    
    fig1 = px.histogram(filtered_df, x="Total Deaths",
                        title="Histogramme global du nombre total de décès dus aux catastrophes naturelles",
                        nbins=50,
                        log_y=True)
    
    fig2 = px.histogram(filtered_df[(filtered_df["Total Deaths"] >= 0) & 
                                    (filtered_df["Total Deaths"] <= 10000)],
                        x="Total Deaths",
                        title="Histogramme des décès (0 à 10,000) dus aux catastrophes naturelles",
                        nbins=100,
                        log_y=True)
    
    fig3 = px.histogram(filtered_df[(filtered_df["Total Deaths"] >= 0) & 
                                    (filtered_df["Total Deaths"] <= 10000)],
                        x="Total Deaths",
                        color="Disaster Subgroup",
                        title="Histogramme des décès (0 à 10,000) dus aux catastrophes naturelles",
                        nbins=100,
                        log_y=True,
                        hover_data=["Disaster Subgroup"])
    

    filtered_for_heatmap = filtered_df[(filtered_df["Total Deaths"] <= 500) & 
                                   (filtered_df["Total Damages ('000 US$)"] <= 1000000)]
    # Histogramme 2D pour "Total Deaths" et "Total Damages"
    fig4 = px.density_heatmap(filtered_for_heatmap, 
                          x="Total Deaths", 
                          y="Total Damages ('000 US$)",
                          marginal_x="histogram", 
                          marginal_y="histogram",
                          title="Densité de la distribution des décès et des dommages",
                          nbinsx=6,  # Utilisation de num_bins pour l'axe x
                          nbinsy=6   # Utilisation de num_bins pour l'axe y
                        )
    fig4.add_trace(px.scatter(filtered_for_heatmap, 
               x="Total Deaths", 
               y="Total Damages ('000 US$)",
               opacity=0.5  # Rendre les points semi-transparents pour améliorer la visibilité
              ).data[0]
    )

    
    return fig1, fig2, fig3, fig4

def generate_graph3_content():
    return html.Div([
        html.H3("Graphique 3"),
        # (Insérez votre graphique 3 ou autres éléments ici)
    ])

def generate_graph4_content():
    return html.Div([
        html.H3("Graphique 4"),
        # (Insérez votre graphique 4 ou autres éléments ici)
    ])

