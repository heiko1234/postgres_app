import dash
import datetime

import pandas as pd
from time import sleep
from dash import html, dcc
from dash import dash_table
from dash import ctx
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px
import plotly

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
    budget_paretoplot,
    sorted_gant
)



dash.register_page(__name__,)

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


analysis_timer = dcc.Interval(id ="booking_timer",  interval = 4*1000)  #1000 ms * 4 = 4sec


date = datetime.datetime.today().strftime('%Y-%m-%d')


# what is this year when loading
this_year=datetime.datetime.today().year
this_month=datetime.datetime.today().month


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
    id="analysis_card",
    title="Project Overview",
    size="1500px", 
    height="650px",
    content=[
        html.Div(
            children=[
                html.Div(children=[
                    mini_card("Year", 
                        a_function=dcc.Dropdown(
                            id="analysis_year",
                            options=years_options,
                            value=this_year 
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
                        dcc.Loading(id="fig_budget")
                    ]
                )
            ],
            style={"display": "block"}
        ),
        analysis_timer
    ]
)


project_card = content_card_size(
    id="analysis_project_card",
    title="Project Planning",
    size="1500px", 
    height="650px",
    content=[
        html.Div(
            children=[
                html.Div(
                    [
                        dcc.Loading(id="fig_project_planning")
                    ]
                )
            ],
            style={"display": "block"}
        ),
    ]
)


layout = html.Div(
    children=[
        html.Div(children=[
            table_card,
        ],
        style={"display": "flex"}),
        html.Div(children=[
            project_card
        ],
        style={"display": "flex"}),
    ],
    style={"display": "block"}
)



# callback

@dash.callback(
    Output("fig_budget", "children"),
    [
        Input("analysis_year", "value"),
    ]
)
def update_founding(year):

    low_year = f"{str(int(year))}"+"-01-01"
    upper_year = f"{str(int(year)+1)}"+"-01-01"


    sql = f"""
            SELECT p.project_id, p.start_date, p.end_date, p.topic, tc.topic_class, p.project_status, pbp.year, pbp.budget
            FROM project p
            INNER JOIN founding_sources fs
            ON p.funding_id = fs.founding_source_id
            INNER JOIN topic_class tc
            ON p.topic_class_id = tc.topic_class_id
            INNER JOIN project_budget_planning pbp
            ON pbp.project_id = p.project_id
            WHERE
            p.end_date > '{low_year}'
            AND
            p.start_date < '{upper_year}'
    """


    data=execute_sql(sql=sql)
    data

    data = pd.DataFrame(data=data, columns = ["project_id", "Start", "Finish", "Task", "Topic", "status", "year", "budget"])

    data = data[data["year"] == year]
    data = data.reset_index(drop = True)

    data = data.groupby(["status"]).sum()

    data = data.reset_index(drop=False)

    try:
        ad = data[data["status"] == "Approved"]
        ad = ad.reset_index(drop=True)
        ad = ad["budget"][0]
    except BaseException:
        ad = 0.001

    try:
        ao = data[data["status"] == "Ongoing"]
        ao = ao.reset_index(drop=True)
        ao = ao["budget"][0]
    except BaseException:
        ao = 0.001

    try:
        ap = data[data["status"] == "Planned"]
        ap = ap.reset_index(drop=True)
        ap = ap["budget"][0]
    except BaseException:
        ap = 0.001

    try:
        ac = data[data["status"] == "Completed"]
        ac = ac.reset_index(drop=True)
        ac = ac["budget"][0]
    except BaseException:
        ac = 0.001


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
    df
    df = df[df["Year"] == year]
    df
    dc = df["Coverage"].sum()  #580

    fig = go.Figure(go.Waterfall(
        name = "Project Waterfall", orientation="v",
        x = ["Approved", "Ongoing", "Completed", "Total Available", "Needed"],
        y = [ad, ao, ac, 0, -dc],
        measure = ["relative", "relative", "relative", "total", "relative"],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
            title = "Plan of Bookings",
            showlegend = True
    )

    return dcc.Graph(figure=fig)



@dash.callback(
    Output("fig_project_planning", "children"),
    [
        Input("analysis_year", "value"),
    ]
)
def update_project_planning(year):

    low_year = f"{str(int(year))}"+"-01-01"
    upper_year = f"{str(int(year)+1)}"+"-01-01"


    sql = f"""
            SELECT p.project_id, tm.full_name, p.start_date, p.end_date, p.topic, tc.topic_class
            FROM project p
            INNER JOIN founding_sources fs
            ON p.funding_id = fs.founding_source_id
            INNER JOIN topic_class tc
            ON p.topic_class_id = tc.topic_class_id
            INNER JOIN project_team_members ptm
            ON p.project_id = ptm.project_id
            INNER JOIN team_members tm
            ON tm.team_id = ptm.team_id
            WHERE
            p.end_date > '{low_year}'
            AND
            p.start_date < '{upper_year}'
    """


    data=execute_sql(sql=sql)
    data


    data = pd.DataFrame(data=data, columns = ["project_id", "fullname", "Start", "Finish", "Task", "Topic"])
    data

    fig = sorted_gant(df=data, Task="Task", team_member="fullname", start_date="Start", end_date="Finish", date=date, plot = False)

    return dcc.Graph(figure=fig)









