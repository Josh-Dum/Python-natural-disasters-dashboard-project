import dash
from config import *
from layout import layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)

from callbacks import *

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)


