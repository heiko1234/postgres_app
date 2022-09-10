import dash
from dash import html, dcc
from app.utilities.cards import (
    mini_card,
    medium_card,
    content_card,
    icon_card
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
    title="Team",
    content=[
        html.Div(
            children=[
                mini_card("Name", a_function=dcc.Input(id="i_name", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Surname", a_function=dcc.Input(id="i_surname", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Full Name", a_function=dcc.Loading(id="o_fullname", style={"width": "130px"})),
                mini_card("BASF UserID", a_function=dcc.Input(id="i_basfid", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Email", a_function=dcc.Input(id="i_mail", type="email", placeholder="", style={"width": "130px"})),
                mini_card("Legal Entity", a_function=dcc.Input(id="i_entity", type="text", placeholder="", style={"width": "130px"})),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                # icon_card(id="test_card", title="Title", text="my text", icon="increase", color="green"),
                html.Button('Save', id='button-save', n_clicks=0, style={"width": "130px", "height": "50px",'font-size': '20px'}),
            ]
        )
    ]
)




layout = html.Div(
    children=[
        team_card,
    ],
)



