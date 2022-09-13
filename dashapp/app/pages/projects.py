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



aproject_card = content_card_size(
    id="project_content",
    title="Project",
    size="1420px", 
    height="900px",
    content=[
        html.Div(
            children=[
                mini_card("Project_ID", a_function=dcc.Input(id="new_projectid", type="text", placeholder="", style={"width": "130px"})),
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
                mini_card("Rec. Account", a_function=dcc.Input(id="new_account", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Cost Center Resp.", a_function=dcc.Input(id="new_account_responsible", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Start Date", a_function=dcc.Input(id="new_start", type="text", placeholder="", style={"width": "130px"})),
                mini_card("End Date", a_function=dcc.Input(id="new_end", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Difficulty", a_function=dcc.Input(id="new_project_diff", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Project Status", a_function=dcc.Input(id="new_project_start", type="text", placeholder="", style={"width": "130px"})),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                content_card_size(
                    id="sub_card",
                    title="Project Description",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Input(id="new_text", type="text", style={"width": "600px", "height": "200px"}))
                    ]
                ),
                content_card_size(
                    id="sub_card2",
                    title="Projects Targets and Goals",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Input(id="new_target", type="text", style={"width": "600px", "height": "200px"}))
                    ]
                ),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                content_card_size(
                    id="sub_card3",
                    title="Project Team",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Loading(id="table_team"))
                    ]
                ),
                content_card_size(
                    id="sub_card4",
                    title="Project Deadlines",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Loading(id="table_deadlines"))
                    ]
                ),
            ],
            style={"display": "flex"}
        )
    ]
)


asign_project = content_card_size(
    id="asign_project_content",
    title="Asign a Project to a team member",
    size="500px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Team_Memeber", a_function=dcc.Input(id="new_projectid", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_button", icon="add", color="white"),
                small_icon_card(id="delete_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)

add_deadline = content_card_size(
    id="deadline_project_content",
    title="Add a deadline",
    size="700px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Deadline Date", a_function=dcc.Input(id="new_projectid", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Deadline Topic", a_function=dcc.Input(id="new_projectid", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_button", icon="add", color="white"),
                small_icon_card(id="delete_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)




layout = html.Div(
    children=[

        aproject_card,
        html.Div(
            children=[
                asign_project,
                add_deadline
            ],
            style={"display": "flex"}
        ),
        
    ],
    style={"display": "block"}
)
