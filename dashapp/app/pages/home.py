import dash
import datetime

import pandas as pd
from time import sleep
from dash import html, dcc
from dash import dash_table
from dash import ctx
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px
import plotly

from app.utilities.cards import (
    mini_card,
    medium_card,
    content_card,
    content_card_size,
    main_hex_card_size
)
from app.utilities.hex_cards import (
    hexagon_card
)



dash.register_page(__name__,)

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


initial_hex = hexagon_card(
    id="hex_test",
    icon = "update",
    text = "Test",
)

hex2 = hexagon_card(
    id="hex_test2",
    icon = "flask",
    text = "Grosser String",
)


layout = html.Div(
    children=[
        main_hex_card_size(
            id="hex_body",
            content=
                [
                    initial_hex,
                    hex2
                ]
        )
    ],
    style={"display": "block"}
)







