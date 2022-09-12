import dash
import datetime

import pandas as pd
from time import sleep
from dash import html, dcc
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app.utilities.cards import (
    mini_card,
    medium_card,
    content_card,
    icon_card,
    icon_action_card,
    small_icon_card,
    content_card_size
)
from app.utilities.app_utilities import (
    get_option_list,
    execute_sql
)


dash.register_page(__name__,)

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )




# what is this year when loading
this_year=datetime.datetime.today().year


add_founding_card = content_card_size(
    id="add_founding_content",
    title="Add an Founding Source",
    size="400px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Founding Source", a_function=dcc.Input(id="add_founding_source", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_source_button", icon="add", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)

add_topic_class_card = content_card_size(
    id="add_topic_class_content",
    title="Add an Topic Class",
    size="400px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Topic Class", a_function=dcc.Input(id="add_topic_class", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_topic_button", icon="add", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)



aproject_card = content_card_size(
    id="project_content",
    title="Project",
    size="1200px", 
    height="700px",
    content=[
        html.Div(
            children=[
                mini_card("Funding", a_function=dcc.Input(id="new_funding", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Topic", a_function=dcc.Input(id="new_topic", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Topic Class", a_function=dcc.Input(id="new_topic_class", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Argus enabled", a_function=dcc.Input(id="new_argus", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Way of charging", a_function=dcc.Input(id="new_charging", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_entity_button", icon="add", color="white"),
                small_icon_card(id="update_project", icon="update", color="white"),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                content_card_size(
                    id="sub_card",
                    title="Description",
                    size="750px", 
                    height="500px",
                    content=[
                        html.Div(dcc.Input(id="new_text", type="text", style={"width": "700px", "height": "450px"}))
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                mini_card("Rec. Account", a_function=dcc.Input(id="new_account", type="text", placeholder="", style={"width": "130px"})),
                                mini_card("Cost Center Resp.", a_function=dcc.Input(id="new_account_responsible", type="text", placeholder="", style={"width": "130px"})),
                            ],
                            style={"display": "flex"}
                        ),
                        html.Div(
                            children=[
                                mini_card("Start Date", a_function=dcc.Input(id="new_start", type="text", placeholder="", style={"width": "130px"})),
                                mini_card("End Date", a_function=dcc.Input(id="new_end", type="text", placeholder="", style={"width": "130px"})),
                            ],
                            style={"display": "flex"}
                        ),
                        html.Div(
                            children=[
                                mini_card("Difficulty", a_function=dcc.Input(id="new_project_diff", type="text", placeholder="", style={"width": "130px"})),
                                mini_card("Total Budget", a_function=dcc.Input(id="new_budget", type="text", placeholder="", style={"width": "130px"})),
                            ],
                            style={"display": "flex"}
                        ),
                        html.Div(
                            children=[
                                mini_card("Project Status", a_function=dcc.Input(id="new_project_start", type="text", placeholder="", style={"width": "130px"})),
                                mini_card("Project_ID", a_function=dcc.Input(id="new_projectid", type="text", placeholder="", style={"width": "130px"})),
                            ],
                            style={"display": "flex"}
                        ),
                    ],
                    style={"display": "block"}
                ),
            ],
            style={"display": "flex"}
        ),
    ]
)


asign_project = content_card_size(
    id="asign_project_content",
    title="Asign a Project to a team member",
    size="1200px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("asign_Project_ID", a_function=dcc.Input(id="new_projectid", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Team_Memeber", a_function=dcc.Input(id="new_projectid", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_button", icon="add", color="white"),
                small_icon_card(id="delete_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)



layout = html.Div(
    children=[
        html.Div(
            children=[
                add_founding_card,
                add_topic_class_card,
            ],
            style={"display": "flex"}
        ),
        aproject_card,
        asign_project
    ],
    style={"display": "block"}
)
