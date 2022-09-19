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


# teammembers: fullname Dropdown
sql = """
    SELECT full_name FROM team_members
"""
data = execute_sql(sql)
data=pd.DataFrame(data, columns=["full_name"])
list_data=list(data["full_name"])
list_data.sort()
team_members_options = get_option_list(list_data)



# years dropdown
sql = f"""
    SELECT YEAR FROM project_budget_planning
"""

data = execute_sql(sql)
data=pd.DataFrame(data, columns=["Year"])
list_data = list(set(data["Year"]))
list_data.sort()
years_options = get_option_list(list_data)


table_card = content_card_size(
    id="table_card_projects_overview_content",
    title="Project Overview",
    size="1500px", 
    height="400px",
    content=[
        html.Div(
            children=[
                html.Div(children=[
                    mini_card("Year", 
                        a_function=dcc.Dropdown(
                            id="overview_year",
                            options=years_options,
                            value=this_year 
                            )
                        ),
                    mini_card("Team Member", 
                        a_function=dcc.Dropdown(
                            id="overview_teammember", 
                            options=team_members_options
                            )
                        ),
                    small_icon_card(id="add_button", icon="add", color="white"),
                    small_icon_card(id="update_button", icon="update", color="white"),
                    ],
                    style={"display": "flex"}
                ),
                html.H3(""),
                dcc.Markdown("\n---\n"),
                html.H3(""),
                html.Div(
                    [
                        dcc.Loading(id="table_overview_overview")
                    ]
                )
            ],
            style={"display": "block"}
        ),
    ]
)


monthly_working = content_card_size(
    id="monthly_working_content",
    title="Monthly Working Days",
    size="900px", 
    height="300px",
    content=[
        html.Div(
            children=[
                html.P("Each month has 20 working days")
            ],
            style={"display": "flex"}
        ),
        html.H3(""),
        dcc.Markdown("\n---\n"),
        html.H3(""),
        html.Div(
            children=[
                html.Div(id="monthly_working")
            ]
        )
    ]
)

monthly_budget = content_card_size(
    id="monthly_budget_content",
    title="Monthly budget Days",
    size="900px", 
    height="300px",
    content=[
        html.Div(
            children=[
                html.P("Gets multiplied with the factor from Entity for each project")
            ],
            style={"display": "flex"}
        ),
        html.H3(""),
        dcc.Markdown("\n---\n"),
        html.H3(""),
        html.Div(
            children=[
                html.Div(id="monthly_budget")
            ]
        )
    ]
)


layout = html.Div(
    children=[
        table_card,
        html.Div(children=[
            monthly_working,
            monthly_budget
        ],
        style={"display": "flex"})
    ],
    style={"display": "block"}
)



@dash.callback(
    Output("table_overview_overview", "children"),
    [
        Input("overview_year", "value"),
        Input("overview_teammember", "value"),
    ]
    # ,prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def overview_table(overview_year, overview_teammember):

    sql=f"""
        SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.project_description
        FROM project p
        INNER JOIN founding_sources fs
        ON p.funding_id = fs.founding_source_id
        INNER JOIN topic_class tc
        ON p.topic_class_id = tc.topic_class_id
        INNER JOIN project_team_members ptm
        ON p.project_id = ptm.project_id
        INNER JOIN team_members tm
        ON tm.team_id = ptm.team_id
        INNER JOIN project_budget_planning pbp
        ON pbp.project_id = p.project_id
        WHERE pbp.year = '{overview_year}'
        AND
        tm.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    """
    data=execute_sql(sql)

    data = pd.DataFrame(data, columns=["project_id", "Topic", "Topic_Class", "Founding Source", "Project Desc."])

    data = data.sort_values(by="project_id")

    df_projects = dash_table.DataTable(
        id = "overview_project_table",
        columns=[{"name": str(i), "id": str(i)} for i in data.columns],
        data=data.to_dict("records"),
        style_table={"height": "300px", "overflow": "auto", "width": "1300px"},
        style_as_list_view=True,
        style_header={"fontweight": "bold", "font-family": "sans-serif"},
        style_cell={
            "font-family": "sans-serif", 
            'overflow': 'hidden',
            "minWidth": 60
            },
        row_selectable="single",
    )

    return df_projects



@dash.callback(

    Output("monthly_working", "children"),
    [
        Input("overview_year", "value"),
        Input("add_button", "n_clicks"),
        Input("update_button", "n_clicks"),
    ]
    # ,prevent_initial_call=True
    # , suppress_callback_exceptions=True
)
def update_project_budget_table(budget_year, add_button, update_button):

    monthly_data = [None,None, None, None, None, None, None, None, None, None, None, None]

    year_data = [budget_year]

    all_data = year_data + monthly_data


    data = pd.DataFrame(data=[all_data], columns = ["Year", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])


    data = data.sort_values(by="Year")

    df_budget_table = dash_table.DataTable(
        id = "project_monthly_budget_table",
        columns=[{"name": str(i), "id": str(i)} for i in data.columns],
        data=data.to_dict("records"),
        style_table={"height": "100px", "overflow": "auto", "width": "850px"},
        style_as_list_view=False,  #True
        editable=True,
        style_header={"fontweight": "bold", "font-family": "sans-serif"},
        style_cell={
            "font-family": "sans-serif", 
            'overflow': 'hidden',
            "minWidth": 60
            },
        row_selectable=False,
    )

    return df_budget_table





