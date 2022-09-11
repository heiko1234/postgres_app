import dash
from dash import html, dcc
from app.utilities.cards import (
    mini_card,
    medium_card,
    content_card,
    icon_card,
    icon_action_card,
    small_icon_card
)

dash.register_page(__name__,)

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )




team_card = content_card(
    id="team_content",
    title="New Team Member",
    content=[
        html.Div(
            children=[
                mini_card("", a_function=None),
                mini_card("Name", a_function=dcc.Input(id="i_name", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Surname", a_function=dcc.Input(id="i_surname", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Full Name", a_function=dcc.Loading(id="o_fullname", style={"width": "130px"})),
                mini_card("BASF UserID", a_function=dcc.Input(id="i_basfid", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Email", a_function=dcc.Input(id="i_mail", type="email", placeholder="", style={"width": "130px"})),
                mini_card("Legal Entity", a_function=dcc.Dropdown(id="i_entity", placeholder="", style={"width": "130px"})),
                small_icon_card(id="save_new", icon="add-user", color="white")
            ],
            style={"display": "flex"}
        ),
    ]
)


update_team_card = content_card(
    id="team_update_content",
    title="Update Team Member",
    content=[
        html.Div(
            children=[
                mini_card("ID", a_function=dcc.Dropdown(id="dd_db_userid", placeholder="", style={"width": "130px"})),
                mini_card("Name", a_function=dcc.Input(id="u_name", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Surname", a_function=dcc.Input(id="u_surname", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Full Name", a_function=dcc.Loading(id="u_fullname", style={"width": "130px"})),
                mini_card("BASF UserID", a_function=dcc.Dropdown(id="dd_basfid", placeholder="", style={"width": "130px"})),
                mini_card("Email", a_function=dcc.Input(id="u_mail", type="email", placeholder="", style={"width": "130px"})),
                mini_card("Legal Entity", a_function=dcc.Dropdown(id="u_entity", placeholder="", style={"width": "130px"})),
                small_icon_card(id="update_new", icon="update", color="white"),
                small_icon_card(id="delete", icon="delete_user", color="white")
            ],
            style={"display": "flex"}
        ),
    ]
)



manage_team_card = content_card(
    id="team_manage_content",
    title="Manage Team Member",
    content=[
        html.Div(
            children=[
                mini_card("ID", a_function=dcc.Dropdown(id="dd_m_userid", placeholder="", style={"width": "130px"})),
                mini_card("Full Name", a_function=dcc.Dropdown(id="m_fullname", style={"width": "130px"})),
                mini_card("BASF UserID", a_function=dcc.Dropdown(id="m_basfid", placeholder="", style={"width": "130px"})),
                mini_card("Contract Year", a_function=dcc.Dropdown(id="m_contract_year", placeholder="", style={"width": "130px"})),
                mini_card("Contract", a_function=dcc.Input(id="m_contract", type="number", min=0, max=100, placeholder="", style={"width": "130px"})),
                mini_card("Budget", a_function=dcc.Loading(id="m_budget", style={"width": "130px"})),
                mini_card("Activty", a_function=dcc.Dropdown(id="m_activity", placeholder="", style={"width": "130px"})),
                small_icon_card(id="update_m", icon="update", color="white"),

            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                # icon_card(id="test_card", title="Title", text="my text", icon="increase", color="green"),
            ]
        )
    ]
)




layout = html.Div(
    children=[
        team_card,
        update_team_card,
        manage_team_card
    ],
    style={"display": "block"}
)



