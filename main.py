import dash
from config import *
from layout import layout

import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])#suppress_callback_exceptions=True)

from callbacks import *

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)


