import dash


import pandas as pd
from time import sleep
from datetime import datetime
from dash import html, dcc
from dash import dash_table
from dash import ctx
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
this_year=datetime.today().year



table_card = content_card_size(
    id="table_card_projects_content",
    title="Project Overview",
    size="1500px", 
    height="500px",
    content=[
        html.Div(
            children=[
                html.Div(children=[
                    mini_card("Year", 
                        a_function=dcc.Dropdown(
                            id="projects_planning_year", 
                            value=this_year
                            )
                        ),
                    mini_card("Team Member", 
                        a_function=dcc.Dropdown(
                            id="projects_planning_teammember", 
                            )
                        ),
                    ],
                    style={"display": "flex"}
                ),
                html.H3(""),
                dcc.Markdown("\n---\n"),
                html.H3(""),
                html.Div(
                    [
                        dcc.Loading(id="table_projects_planning_overview")
                    ]
                )
            ],
            style={"display": "block"}
        ),
    ]
)


gant_card = content_card_size(
    id="gant_card_projects_planning_content",
    title="Project Timeline",
    size="1500px", 
    height="480px",
    content=[
        html.Div(
            [dcc.Loading(id="fig_project_planning_timeline")]
        )
    ]
)

project_card = content_card_size(
    id="planning_project_card",
    title="Project Planning",
    size="1500px", 
    height="650px",
    content=[
        html.Div(
            children=[
                html.Div(
                    [
                        dcc.Loading(id="planning_fig_project_planning")
                    ]
                )
            ],
            style={"display": "block"}
        ),
    ]
)


layout = html.Div(
    children=[
        table_card,
        gant_card,
        project_card
    ]
)




