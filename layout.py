from dash import dcc, html

layout = html.Div([
    # Menu sur le côté gauche
    html.Div([
        dcc.Tabs(id='tabs', value='home', children=[
            dcc.Tab(label='Home', value='home'),
            dcc.Tab(label='Cartes des catastrophes', value='map'),
            dcc.Tab(label='Histogrammes des morts', value='histogram'),
            dcc.Tab(label='Graphique 3', value='graph3'),
            dcc.Tab(label='Graphique 4', value='graph4'),
        ]),
    ], style={'width': '20%', 'float': 'left'}),

    # Contenu principal
    html.Div(id='content', style={'width': '75%', 'float': 'right'})
])