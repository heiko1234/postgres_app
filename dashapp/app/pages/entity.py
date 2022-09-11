import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
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
    get_option_list
)

dash.register_page(__name__,)

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


add_entity_card = content_card_size(
    id="add_entity_content",
    title="Add an Entity",
    size="400px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Legal Entity", a_function=dcc.Input(id="add_entity", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_entity_button", icon="add", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


update_coverage_entity = content_card_size(
    id="add_entity_content",
    title="Update Entity Coverage",
    size="800px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Legal Entity", a_function=dcc.Dropdown(id="dd_entity", style={"width": "130px"})),
                mini_card("Year", a_function=dcc.Input(id="dd_year", type="number", min=2000, max=2100, step=1, value=2024, style={"width": "130px"})),
                mini_card("Coverage", a_function=dcc.Input(id="coverage_entity", type="number", min=0, max=1000, value=200, style={"width": "130px"})),
                small_icon_card(id="update_entity", icon="update", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


table_card = content_card_size(
    id="table_card_content",
    title="Yearly Coverage of Entities",
    size="1224px", 
    height="500px",
    content=[
        html.Div(
            children=[
                html.Div(
                    [
                        small_icon_card(id="table_card_update", icon="simple_update", color="white"),
                        dcc.Loading(id="table_card_id")
                    ]
                )
            ],
            style={"display": "block"}
        ),
    ]
)



layout = html.Div(
    children=[
        html.Div(
            children=[
                add_entity_card,
                update_coverage_entity
            ],
            style={"display": "flex"}
        ),
        table_card
    ],
    style={"display": "block"}
)



@dash.callback(
    Output("a_session_store", "data"),
    [
        Input("add_entity_button_button", "n_clicks"),
        State("add_entity", "value"),
    ]
)
def new_entity(n_clicks, new_entity):

    return new_entity


@dash.callback(
    [
        Output("dd_entity", "options"),
        Output("dd_entity", "value")
    ],
    [
        Input("a_session_store", "data"),
    ]
)
def new_entity(data):

    dict_list = get_option_list(data)

    first_choise = data[0]

    return dict_list, first_choise
