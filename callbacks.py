import folium
import plotly_express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import geopandas as gpd

from config import *

from main import app

@app.callback(
    Output('content', 'children'),
    [Input("home-link", "n_clicks"),
     Input("map-link", "n_clicks"),
     Input("histogram-link", "n_clicks"),
     Input("graph3-link", "n_clicks"),
     Input("graph4-link", "n_clicks")]
)
def update_content(home_link_clicks, map_link_clicks, histogram_link_clicks, graph3_link_clicks, graph4_link_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return generate_home_content()
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "home-link":
            return generate_home_content()
        elif button_id == "map-link":
            return generate_map_content()
        elif button_id == "histogram-link":
            return generate_histogram_content()
        elif button_id == "graph3-link":
            return generate_graph3_content()
        elif button_id == "graph4-link":
            return generate_graph4_content()
        

def generate_home_content():
    return html.Div([
        html.H2("Bienvenue sur le Dashboard",style={'textAlign': 'center'},
            className= 'subtitle_color'),
        # (Insérez votre graphique 4 ou autres éléments ici)
    ])

    # Définition de la fonction de mise à jour en réponse à la sélection de l'utilisateur
def generate_map_content():
    # Votre code pour générer la carte
    return html.Div(children=[
        html.H2(children=f'Carte des catastrophes naturelles',style={'textAlign': 'center',},
            className= 'subtitle_color'),
        dcc.RangeSlider(id='annees',
                        className='RangeSlider',
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
    carte = folium.Map(location = coord, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', attr='ESRI', zoom_start=3)

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
    html.H2(children='Histogramme des décès dus aux catastrophes naturelles',
            style={'textAlign': 'center'},
            className= 'subtitle_color'),
    
    # RangeSlider pour sélectionner la plage d'années
    dcc.RangeSlider(
        id='year-slider',
        className='RangeSlider',
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
    ''', className= 'description_color text-center p-3 marge_top')
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
        html.H2("Graphique 3",style={'textAlign': 'center',},
            className= 'subtitle_color'),
        # (Insérez votre graphique 3 ou autres éléments ici)
    ])

def generate_graph4_content():
    return html.Div(children=[
        html.H2(children=f'Carte catastrophe',style={'textAlign': 'center',},
            className= 'subtitle_color'),
        dcc.RangeSlider(id='range_annees',
                        className='RangeSlider',
                        marks={str(year): str(year) for year in annees if year %10 == 0},
                        min=min(annees),
                        max=max(annees),
                        value=[max(annees)-1, max(annees)],
                        step=1,
                        tooltip={"placement":"bottom","always_visible":True}),
        html.Div(id='map_2'),
        html.H3(children = f'''
                On peut décocher et cocher en haut a droite pour voir seulement le nombre de catastrophes par pays ou le nombres de morts par pays.
                ''', className='description_color text-center p-3 marge_top')
    ])

@app.callback(
    Output('map_2', 'children'),
    [Input('range_annees', 'value')]
)
def update_map_2(year_range):
    coord = (48.8398094, 2.5840685) # centré sur l'Esiee
    carte = folium.Map(location = coord,tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', attr='ESRI',zoom_start=3)

    debut , fin = year_range


    df_filtered = disaster_counts[(disaster_counts['Year'] >= debut) & (disaster_counts['Year'] <= fin)]

    # Calcule le nombre total de catastrophes par pays sur la plage d'années sélectionnée
    country_disaster_counts = df_filtered.groupby('ISO')['Disaster Count'].sum().reset_index()
    # Utiliser Choropleth pour colorer les pays en fonction du nombre de catastrophes
    folium.Choropleth(
        geo_data=country_geojson,
        name='Nombre de castrophes naturelles par pays',
        data=country_disaster_counts,
        columns=['ISO', 'Disaster Count'],
        key_on='feature.properties.ISO_A3',  # Assurez-vous que cette propriété correspond à votre GeoJSON
        fill_color='OrRd',  # Choisissez une palette de couleurs
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Nombre de catastrophes naturelles par pays'
    ).add_to(carte)


    df_filtered_death = disaster_death_counts[(disaster_death_counts['Year'] >= debut) & (disaster_death_counts['Year'] <= fin)]
    country_death_counts = df_filtered_death.groupby('ISO')['Death Count'].sum().reset_index()

    folium.Choropleth(
        geo_data=country_geojson,
        name='Nombre de morts par pays',
        data=country_death_counts,
        columns=['ISO', 'Death Count'],
        key_on='feature.properties.ISO_A3',  # Assurez-vous que cette propriété correspond à votre GeoJSON
        fill_color='YlOrRd',  # Choisissez une palette de couleurs
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Nombre de morts par pays'
    ).add_to(carte)

    folium.LayerControl().add_to(carte)



    # Enregistre la carte dans un fichier HTML et la retourne pour l'affichage dans Dash
    carte_html = carte._repr_html_()
    return html.Iframe(srcDoc=carte_html, width='100%', height='600px')