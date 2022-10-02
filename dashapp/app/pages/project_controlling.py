import dash
import datetime

import pandas as pd
from time import sleep
from dash import html, dcc
from dash import dash_table
from dash import ctx
import dash_daq as daq
import plotly.express as px
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

from app.utilities.plot import (
    budget_paretoplot
)



dash.register_page(__name__,)

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


controlling_timer = dcc.Interval(id ="booking_timer",  interval = 4*1000)  #1000 ms * 4 = 4sec




# what is this year when loading
this_year=datetime.datetime.today().year
this_month=datetime.datetime.today().month


# months drop down
month_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
month_options = get_option_list(month_list)



# years dropdown
sql = f"""
    SELECT YEAR FROM project_budget_planning
"""

data = execute_sql(sql)
data=pd.DataFrame(data, columns=["Year"])
list_data = list(set(data["Year"]))
list_data.sort()
years_options = get_option_list(list_data)


# project status
project_status=get_option_list(["Planned", "Approved", "Ongoing", "Completed", "Rejected"])




table_card = content_card_size(
    id="controling_card",
    title="Project Overview",
    size="1500px", 
    height="700px",
    content=[
        html.Div(
            children=[
                html.Div(children=[
                    mini_card("Year", 
                        a_function=dcc.Dropdown(
                            id="controling_year",
                            options=years_options,
                            value=this_year 
                            )
                        ),
                    mini_card("Month", 
                        a_function=dcc.Dropdown(
                            id="controling_month", 
                            options=month_options,
                            value=this_month
                            )
                        ),
                    medium_card(
                        id="medium_status",
                        text="Project Status", 
                        a_function=dcc.Dropdown(
                            id="controling_status", 
                            options=project_status,
                            value=["Ongoing", "Completed"],
                            multi=True
                            )
                        ),
                    mini_card("Aggregate",
                        a_function=daq.BooleanSwitch(
                            id='aggregation_switch',
                            color="blue", 
                            on=False),
                        ),
                    mini_card("Download",
                        a_function=html.Button(
                            "Download", 
                            id="button_xlsx",
                            style={"width": "100px", "height": "35px"}
                            )
                        )
                    ],
                    style={"display": "flex"}
                ),
                html.H3(""),
                dcc.Markdown("\n---\n"),
                html.H3(""),
                html.Div(
                    [
                        dcc.Loading(id="table_controling")
                    ]
                )
            ],
            style={"display": "block"}
        ),
        controlling_timer
    ]
)


missing_card = content_card_size(
    id="controling_missing_card",
    title="Missing a Costcenter Table",
    size="1500px", 
    height="300px",
    content=[
        html.Div(
            [
                dcc.Loading(id="table_controling_missing")
            ]
        )
    ]
)


layout = html.Div(
    children=[
        html.Div(children=[
            table_card,
            dcc.Download(id="download-dataframe-xlsx"),
        ],
        style={"display": "flex"}),
        missing_card,
    ],
    style={"display": "block"}
)



# callbacks



# show up teammember_table
@dash.callback(
    Output("table_controling", "children"),
    [
        Input("controling_year", "value"),
        Input("controling_month", "value"),
        Input("controling_status", "value"),
        Input("aggregation_switch", "on")
    ]
    # , prevent_initial_call=True
    # , suppress_callback_exceptions=True
)
def update_controlling_table(year, month, status_list, aggregation):

    if ((year != None) and (month != None)):

        sql = f"""
            SELECT ptb.year, ptb.month, ptb.team_id, ptb.project_id, p.topic, p.project_status, ptb.working_booking, tm.full_name, appc.costcenter
            FROM project_time_budget ptb
            INNER JOIN team_members tm
            ON tm.team_id = ptb.team_id
            INNER JOIN active_project_person_costcenter appc
            ON appc.project_id = ptb.project_id AND appc.team_id = ptb.team_id
            INNER JOIN project p
            ON p.project_id = appc.project_id
            WHERE 
            ptb.year = '{year}' 
            AND
            ptb.month = '{month}'
        """

        data=execute_sql(sql)
        data


        data = pd.DataFrame(data, columns=["year", "month", "team_id", "project_id", "topic", "status", "working_booking", "fullname", "Costcenter"])
        data

        if len(status_list) != 0:
            data = data[data["status"].isin(status_list)]

        if aggregation:
            data = data.loc[:,["year", "month", "project_id", "topic", "working_booking", "Costcenter"]]

            data.groupby(["year", "month", 'Costcenter', "project_id", "topic"]).sum()


        table_controling = dash_table.DataTable(
            id = "controling_table",
            columns=[{"name": str(i), "id": str(i)} for i in data.columns],
            data=data.to_dict("records"),
            style_table={"height": "6000px", "overflow": "auto", "width": "1400px"},
            style_as_list_view=True,
            style_header={"fontweight": "bold", "font-family": "sans-serif"},
            style_cell={
                "font-family": "sans-serif", 
                'overflow': 'hidden',
                "minWidth": 60
                },
            row_selectable=False,
        )

    else:
        table_controling = html.H3("No year / no month selected")

    return table_controling




# show up missing values
@dash.callback(
    Output("table_controling_missing", "children"),
    [
        Input("controling_year", "value"),
        Input("controling_month", "value"),
    ]
    # , prevent_initial_call=True
    # , suppress_callback_exceptions=True
)
def update_controlling_missing_table(year, month):

    if ((year != None) and (month != None)):

        sql = f"""
            SELECT ptb.year, ptb.month, ptb.project_id, p.topic, p.project_status, ptb.working_booking, tm.full_name, appc.costcenter
            FROM project_time_budget ptb
            INNER JOIN team_members tm
            ON tm.team_id = ptb.team_id
            INNER JOIN project p
            ON p.project_id = ptb.project_id
            LEFT JOIN active_project_person_costcenter appc
            ON appc.project_id = ptb.project_id AND appc.team_id = ptb.team_id
            WHERE 
            ptb.year = '{year}' 
            AND
            ptb.month = '{month}'
            AND
            appc.costcenter IS NULL

        """

        data=execute_sql(sql)

        data = pd.DataFrame(data, columns=["year", "month", "project_id", "topic", "status", "booking", "name", "costcenter"])

        table_controling = dash_table.DataTable(
            id = "table_missing_controling",
            columns=[{"name": str(i), "id": str(i)} for i in data.columns],
            data=data.to_dict("records"),
            style_table={"height": "250px", "overflow": "auto", "width": "1400px"},
            style_as_list_view=True,
            style_header={"fontweight": "bold", "font-family": "sans-serif"},
            style_cell={
                "font-family": "sans-serif", 
                'overflow': 'hidden',
                "minWidth": 60
                },
            row_selectable=False,
        )

    else:
        table_controling = html.H3("No year / no month selected")

    return table_controling


