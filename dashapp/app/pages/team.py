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


sql = """
    SELECT entity_name FROM entity
"""
data = execute_sql(sql)
data=pd.DataFrame(data, columns=["Entity"])
list_data=list(data["Entity"])
list_data.sort()
entity_options = get_option_list(list_data)


# what is this year when loading
this_year=datetime.datetime.today().year


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
    title="Update or Delete a Team Member",
    content=[
        html.Div(
            children=[
                mini_card("Full Name", a_function=dcc.Dropdown(id="u_fullname", style={"width": "130px"})),
                mini_card("Name", a_function=dcc.Input(id="u_name", type="text", style={"width": "130px"})),
                mini_card("Surname", a_function=dcc.Input(id="u_surname", type="text", style={"width": "130px"})),
                mini_card("UserID", a_function=dcc.Input(id="u_id", type="text", style={"width": "130px"})),
                mini_card("Email", a_function=dcc.Input(id="u_mail", type="email", style={"width": "130px"})),
                mini_card("Legal Entity", a_function=dcc.Dropdown(id="u_entity", options=entity_options, style={"width": "130px"})),
                mini_card("Start Date", a_function=dcc.DatePickerSingle(id="u_contract_year", style={"width": "130px"})),
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
                mini_card("Year", a_function=dcc.Input(id="m_year", type="number", min=2000, max=2100, step=1, value=this_year, style={"width": "130px"})),
                mini_card("Contract", a_function=dcc.Input(id="m_contract", type="number", value=100, min=0, max=100, style={"width": "130px"})),
                mini_card("Working Month", a_function=dcc.Input(id="m_month", type="number", value=12, min=0, max=12, style={"width": "130px"})),
                mini_card("Activty", a_function=dcc.Dropdown(id="m_activity", options=[{"label": "Project", "value": "Project"}, {"label": "Verbund", "value": "Verbund"}], style={"width": "130px"})),
                mini_card("Calculate Budget", a_function=dcc.Loading(id="m_budget", style={"width": "130px"})),
                small_icon_card(id="update_m", icon="update", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


table_card = content_card_size(
    id="table_card_team_content",
    title="Yearly Coverage of Team",
    size="1700px", 
    height="500px",
    content=[
        html.Div(
            children=[
                mini_card("Select", 
                    a_function=dcc.Dropdown(
                        id="team_table_dd", 
                        options=[
                            {"label": "eff. Coverage", "value": "eff. Coverage"},
                            {"label": "Coverage", "value": "Coverage"}, 
                            {"label": "Contract", "value": "Contract"}, 
                            {"label": "Working Month", "value": "Working Month"},
                            {"label": "Activity", "value": "Activity"},
                            ],
                            style={"width": "130px"},
                        value="eff. Coverage",
                        )
                    ),
                html.Div(
                    [
                        dcc.Loading(id="table_team_card_id")
                    ]
                )
            ],
            style={"display": "block"}
        ),
    ]
)




layout = html.Div(
    children=[
        team_card,
        update_team_card,
        manage_team_card,
        table_card
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
    # ,prevent_initial_call=True
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


# update a person

@dash.callback(

    Output("update_new", "style"),
    [
        Input("update_new_button", "n_clicks"),
        State("u_fullname", "value"),
        State("u_name", "value"),
        State("u_surname", "value"),
        State("u_id", "value"),
        State("u_mail", "value"),
        State("u_entity", "value"),
        State("u_contract_year", "date"),
    ]
    ,prevent_initial_call=True
)
def update_person(n_clicks, old_fullname, new_name, new_surname, new_user_id, new_email, new_legal_entity, new_entry_date):

    color = {"background-color": "white"}

    new_fullname = new_name+" "+new_surname

    sql=f"""
            UPDATE team_members
            SET 
            pre_name = '{new_name}',
            sur_name = '{new_surname}',
            full_name = '{new_fullname}',
            email = '{new_email}',
            user_id = '{new_user_id}',
            legal_entity_id = (SELECT entity_id FROM entity WHERE entity_name = '{new_legal_entity}'),
            department_entry_date = '{new_entry_date}'
            WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{old_fullname}');
    """


    data = execute_sql(sql)
    data

    return color




@dash.callback(
    [
        Output("u_name", "value"),
        Output("u_surname", "value"),
        Output("u_id", "value"),
        Output("u_mail", "value"),
        Output("u_entity", "value"),
        Output("u_contract_year", "date"),
    ],
    [
        Input("u_fullname", "value"),
    ]
    ,prevent_initial_call=True
)
def update_dropdown(fullname):

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
        
        u_entry_year = data.loc[0, "entry_date"]



    else:
        u_name = u_surname = u_id = u_mail = u_entity = None 
        u_entry_year = None

    return u_name, u_surname, u_id, u_mail, u_entity, u_entry_year




@dash.callback(

    Output("m_budget", "children"),
    [
        Input("m_fullname", "value"),
        Input("m_year", "value"),
        Input("m_contract", "value"),
        Input("m_month", "value")
    ]
    ,prevent_initial_call=True
)
def update_calculation_budget(fullname, year, contract, month):

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

        budget = float(value) * float(contract) / 100 * month/12

        budget = round(budget, 0)

        return html.H3(budget)

    else: 
        return html.H3("No Data")



@dash.callback(
    Output("table_team_card_id", "children"),
    [
        Input("team_table_dd", "value"),
        Input("update_m_button", "n_clicks"),
    ]
    # ,prevent_initial_call=True
)
def call_datatable(dd_team, n_clicks_update):

    sleep(0.5)

    sql = f"""
        SELECT tm.full_name, ti.year, ti.contract, ti.working_month, ti.activity, et.coverage
        FROM team_members tm
        INNER JOIN team_info ti
        ON tm.team_id = ti.team_id
        INNER JOIN entity_time et
        ON et.entity_id = tm.legal_entity_id and ti.year = et.year
    """
    data = execute_sql(sql)


    df = pd.DataFrame(data, columns=["Fullname", "Year", "Contract", "Working Month", "Activity", "Coverage"])


    df["eff. Coverage"] = round(df["Contract"] * df["Working Month"] * df["Coverage"] * 1/100 * 1/12,1)

    pdf = df.pivot(index = "Fullname", columns="Year", values=dd_team).reset_index(drop=False)

    output_df = dash_table.DataTable(
        id = "table_entity_time",
        columns=[{"name": str(i), "id": str(i)} for i in pdf.columns],
        data=pdf.to_dict("records"),
        style_table={"height": "300px", "overflow": "auto", "width": "1400px"},
        style_as_list_view=True,
        style_header={"fontweight": "bold", "font-family": "sans-serif"},
        style_cell={
            "font-family": "sans-serif", 
            'overflow': 'hidden',
            # 'textOverflow': 'ellipsis',
            # 'maxWidth': 40, 
            "minWidth": 60
            },
        row_selectable=False,
        # selected_rows=[0]
    )

    return output_df






@dash.callback(
    Output("update_m", "style"),
    [
        Input("update_m_button", "n_clicks"),
        State("m_fullname", "value"),
        State("m_year", "value"),
        State("m_contract", "value"),
        State("m_month", "value"),
        State("m_activity", "value")
    ]
    ,prevent_initial_call=True
)
def new_entity(n_clicks, fullname, year, contract, working_month, activity):

    color = {"background-color": "white"}

    sql = f"""
            DELETE from team_info 
            WHERE
            team_id in (SELECT team_id FROM team_members WHERE full_name = '{fullname}')
            AND
            team_info.year = '{int(year)}';
    """
    data=execute_sql(sql = sql)


    sql = f"""
        INSERT INTO team_info (team_id, year, contract, working_month, entity_id, activity) VALUES 
        (
            (SELECT team_id FROM team_members WHERE full_name = '{fullname}'),
            '{int(year)}',
            '{int(contract)}',
            '{int(working_month)}',
            (SELECT legal_entity_id FROM team_members WHERE full_name = '{fullname}'),
            '{activity}'
        );
    """
    data=execute_sql(sql = sql)

    return color






