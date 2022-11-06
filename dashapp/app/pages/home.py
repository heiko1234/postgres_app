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


dash.register_page(__name__, path='/')


# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


hex_team = hexagon_card(
    id="hex_team",
    icon = "user",
    text = "Team",
    href="team"
)

hex_idea = hexagon_card(
    id="hex_idea",
    icon = "idea",
    text = "Project",
    href="projects"
)

hex_booking = hexagon_card(
    id="hex_booking",
    icon = "money1",
    text = "Booking",
    href="booking"
)

hex_analyis = hexagon_card(
    id="hex_analysis",
    icon = "account",
    text = "Analysis",
    href="analysis"
)

hex_controlling = hexagon_card(
    id="hex_controlling",
    icon = "analysis6",
    text = "Controling",
    href="project-controlling"
)

hex_construct = hexagon_card(
    id="hex_construct",
    icon = "construct3",
    text = "Controling",
    href="construct"
)
hex_cost = hexagon_card(
    id="hex_cost",
    icon = "account2",
    text = "Costs",
    href="costcenter"
)
hex_benefit = hexagon_card(
    id="hex_benefit",
    icon = "increase",
    text = "Benefit",
    href="increase"
)
hex_search = hexagon_card(
    id="hex_search",
    icon = "search",
    text = "Search",
    href="search"
)





layout = html.Div(
    children=[
        main_hex_card_size(
            id="hex_body",
            content=
                [
                    hex_team,
                    hex_idea,
                    hex_booking,
                    hex_analyis,
                    hex_controlling,
                    hex_search,
                    hex_construct,
                    hex_cost,
                    hex_benefit
                ]
        )
    ],
    # style={
    #     "display": "block",
    #     "width": "600px",
    #     "height": "800px",
    #     }
)







