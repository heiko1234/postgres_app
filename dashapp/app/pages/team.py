import dash

import pandas as pd
from time import sleep
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app.utilities.cards import (
    mini_card,
    medium_card,
    content_card,
    icon_card,
    icon_action_card,
    small_icon_card
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


sql = """
    SELECT entity_name FROM entity
"""
data = execute_sql(sql)
data=pd.DataFrame(data, columns=["OD"])
list_data=list(data["OD"])
list_data.sort()
entity_options = get_option_list(list_data)




team_card = content_card(
    id="team_content",
    title="New Team Member",
    content=[
        html.Div(
            children=[
                mini_card("", a_function=None),
                mini_card("Name", a_function=dcc.Input(id="i_name", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Surname", a_function=dcc.Input(id="i_surname", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Full Name", a_function=html.Div(id="o_fullname", style={"width": "130px"})),
                mini_card("UserID", a_function=dcc.Input(id="i_id", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Email", a_function=dcc.Input(id="i_mail", type="email", placeholder="", style={"width": "130px"})),
                mini_card("Legal Entity", a_function=dcc.Dropdown(id="i_entity", options=entity_options, style={"width": "130px"})),
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
                mini_card("Full Name", a_function=dcc.Dropdown(id="u_fullname", style={"width": "130px"})),
                mini_card("Name", a_function=dcc.Input(id="u_name", type="text", style={"width": "130px"})),
                mini_card("Surname", a_function=dcc.Input(id="u_surname", type="text", style={"width": "130px"})),
                mini_card("UserID", a_function=dcc.Input(id="u_id", type="text", style={"width": "130px"})),
                mini_card("Email", a_function=dcc.Input(id="u_mail", type="email", style={"width": "130px"})),
                mini_card("Legal Entity", a_function=dcc.Dropdown(id="u_entity", options=entity_options, style={"width": "130px"})),
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
                mini_card("Full Name", a_function=dcc.Dropdown(id="m_fullname", style={"width": "130px"})),
                mini_card("Contract Year", a_function=dcc.DatePickerSingle(id="m_contract_year", style={"width": "130px"})),
                mini_card("Contract", a_function=dcc.Input(id="m_contract", type="number", value=100, min=0, max=100, style={"width": "130px"})),
                mini_card("Year", a_function=dcc.Input(id="m_year", type="number", min=2000, max=2100, step=1, value=2024, style={"width": "130px"})),
                mini_card("Budget", a_function=dcc.Loading(id="m_budget", style={"width": "130px"})),
                mini_card("Activty", a_function=dcc.Dropdown(id="m_activity", style={"width": "130px"})),
                small_icon_card(id="update_m", icon="update", color="white"),

            ],
            style={"display": "flex"}
        ),
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





@dash.callback(
    [
        Output("i_entity", "value"),
        Output("o_fullname", "children"),
    ],
    [
        Input("save_new_button", "n_clicks"),
        State("i_name", "value"),
        State("i_surname", "value"),
        State("i_id", "value"),
        State("i_mail", "value"),
        State("i_entity", "value"),
    ]
    ,prevent_initial_call=True
)
def new_entity(n_clicks, name, surename, id, mail, entity):

    if ((name != None) and (surename != None)):

        fullname = str(name)+" "+ str(surename)

        sql = f"""
            INSERT INTO team_members (pre_name, sur_name, full_name, user_id, email, legal_entity_id) VALUES 
            ('{name}', '{surename}', '{fullname}', '{id}', '{mail}', (SELECT entity_id FROM entity WHERE entity_name = '{entity}'));
        """

        data = execute_sql(sql)

        entity_value = entity

    else: 
        fullname = None
        entity_value = None

    return entity_value, html.H4(fullname)



@dash.callback(
    
    [
    Output("u_fullname", "options"),
    Output("m_fullname", "options"),
    ],
    [
        Input("save_new_button", "n_clicks"),
    ]
)
def update_dropdown(n_clicks):

    sql = """
        SELECT full_name FROM team_members
    """
    data = execute_sql(sql)

    data=pd.DataFrame(data, columns=["people"])
    list_data=list(data["people"])
    list_data.sort()

    dict_list = get_option_list(list_data)

    return dict_list, dict_list




@dash.callback(

    Output("delete", "style"),
    [
        Input("delete_button", "n_clicks"),
        State("u_fullname", "value"),
    ]
    ,prevent_initial_call=True
)
def delete_person(n_clicks, u_fullname):

    color = {"background-color": "white"}

    sql = f"""
            DELETE from team_members 
            WHERE
            full_name  = '{u_fullname}';
    """

    data=execute_sql(sql = sql)
    data

    return color


# mini_card("Full Name", a_function=dcc.Dropdown(id="u_fullname", style={"width": "130px"})),
# mini_card("Name", a_function=dcc.Input(id="u_name", type="text", style={"width": "130px"})),
# mini_card("Surname", a_function=dcc.Input(id="u_surname", type="text", style={"width": "130px"})),
# mini_card("UserID", a_function=dcc.Input(id="u_id", type="text", style={"width": "130px"})),
# mini_card("Email", a_function=dcc.Input(id="u_mail", type="email", style={"width": "130px"})),
# mini_card("Legal Entity", a_function=dcc.Dropdown(id="u_entity", options=entity_options, style={"width": "130px"})),


@dash.callback(
    [
        Output("u_name", "value"),
        Output("u_surname", "value"),
        Output("u_id", "value"),
        Output("u_mail", "value"),
        Output("u_entity", "value"),
    ],
    [
        Input("u_fullname", "value"),
    ]
    ,prevent_initial_call=True
)
def update_dropdown(fullname):


    # SELECT et.year, e.entity_name, et.coverage
    # FROM entity_time et
    # INNER JOIN entity e
    # ON e.entity_id = et.entity_id;


    # sql = f"""SELECT * FROM team_members WHERE full_name = '{fullname}';
    # """

    if fullname != None:

        sql = f"""
            SELECT tm.pre_name, tm.sur_name, tm.full_name, tm.email, tm.user_id, e.entity_name, tm.department_entry_date
            FROM team_members tm
            INNER JOIN entity e
            ON tm.legal_entity_id = e.entity_id
            WHERE tm.full_name = '{fullname}';
        """

        data = execute_sql(sql)

        data=pd.DataFrame(data, columns=["pre_name", "sur_name", "full_name", "email", "user_id", "leagal_entity", "entry_date"])
        data = data.reset_index(drop = True)

        u_name = data.loc[0, "pre_name"]
        u_surname = data.loc[0, "sur_name"]
        u_id = data.loc[0, "user_id"]
        u_mail = data.loc[0, "email"]
        u_entity = data.loc[0, "leagal_entity"]

    else:
        u_name = u_surname = u_id = u_mail = u_entity = None

    return u_name, u_surname, u_id, u_mail, u_entity




@dash.callback(

    Output("m_budget", "children"),
    [
        Input("m_fullname", "value"),
        Input("m_year", "value"),
        Input("m_contract", "value")
    ]
    ,prevent_initial_call=True
)
def update_dropdown(fullname, year, contract):

    sleep(0.5)


    if ((fullname != None) and (year != None) and (contract != None)):

        sql = f"""
            SELECT tm.full_name, e.entity_name, et.year, et.coverage
            FROM team_members tm
            INNER JOIN entity e
            ON tm.legal_entity_id = e.entity_id
            INNER JOIN entity_time et
            ON e.entity_id = et.entity_id
            WHERE ((tm.full_name = '{fullname}') AND (et.year = '{year}'));
        """


        data = execute_sql(sql)

        data = pd.DataFrame(data, columns=["fullname", "entity", "year", "budget"])

        value = data.loc[0, "budget"]

        budget = float(value) * float(contract) / 100

        budget = round(budget, 0)

        return html.H3(budget)

    else: 
        return html.H3("A Problem")





