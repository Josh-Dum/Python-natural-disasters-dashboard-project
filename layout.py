from dash import dcc, html
import dash_bootstrap_components as dbc

# Sidebar
sidebar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/home", id="home-link", style={"font-size": "20px", "margin-bottom": "10px"})),
        dbc.NavItem(dbc.NavLink("Cartes des catastrophes", href="/map", id="map-link", style={"font-size": "20px", "margin-bottom": "10px"})),
        dbc.NavItem(dbc.NavLink("Histogrammes des morts", href="/histogram", id="histogram-link", style={"font-size": "20px", "margin-bottom": "10px"})),
        dbc.NavItem(dbc.NavLink("L'évolution des catastrophes", href="/graph3", id="graph3-link", style={"font-size": "20px", "margin-bottom": "10px"})),
        dbc.NavItem(dbc.NavLink("Le pays le plus sûr", href="/graph4", id="graph4-link", style={"font-size": "20px", "margin-bottom": "10px"})),
        dbc.NavItem(dbc.NavLink("Catastrophes les plus meurtrières", href="/graph5", id="graph5-link", style={"font-size": "20px", "margin-bottom": "10px"})),
    ],
    vertical=True,
    pills=True,
    className="sidebar text-center bg-dark p-3 shadow-2 marge_top",  # Fond sombre avec ombres et texte clair pour le menu
)

# Titre
title = html.H1("Données sur les catastrophes naturelles", className="mb-4 text-center bg-dark p-3 shadow-2 couleur_titre marge_top")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=2),  # Sidebar a une largeur fixe de 2
                dbc.Col([
                    title,  # Titre au-dessus du contenu
                    html.Div(id='content', className="text-center bg-dark text-light p-3 shadow-2")
                ], width=10),  # Contenu principal prend le reste de l'espace
            ],
            
            className="flex-nowrap",  # Force les colonnes à ne pas passer à la ligne
        ),
    ],
    fluid=True,
    className="d-flex flex-column vh-100 bg-secondary",  # La hauteur est basée sur la hauteur de la fenêtre
)