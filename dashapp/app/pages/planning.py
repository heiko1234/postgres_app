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
    sorted_gant,
    single_gantt
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


# teammembers: fullname Dropdown
sql = """
    SELECT full_name FROM team_members
"""
data = execute_sql(sql)
data=pd.DataFrame(data, columns=["full_name"])
list_data=list(data["full_name"])
list_data.sort()
team_members_options = get_option_list(list_data)



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
                            options=years_options,
                            value=this_year
                            )
                        ),
                    mini_card("Team Member", 
                        a_function=dcc.Dropdown(
                            id="projects_planning_teammember", 
                            options=team_members_options
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


assign_project = content_card_size(
    id="assigned_team",
    title="Assign a Project to Team Members",
    size="750px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Project ID", a_function=dcc.Dropdown(id="planning_projectid", style={"width": "130px"})),
                mini_card("Team Member", a_function=dcc.Dropdown(id="planning_single_teammember", style={"width": "130px"})),
                small_icon_card(id="planning_add_button", icon="add", color="white"),
                small_icon_card(id="planning_delete_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)

shift_project=content_card_size(
    id="shift_project",
    title="Shift a Porject",
    size="600px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Start Date", a_function=dcc.DatePickerSingle(id="planning_start", style={"width": "130px"})),
                mini_card("End Date", a_function=dcc.DatePickerSingle(id="planning_end", style={"width": "130px"})),
                small_icon_card(id="planning_update_button", icon="update", color="white"),
            ],
            style={"display": "flex"}
        )
    ]
)



layout = html.Div(
    children=[
        table_card,
        gant_card,
        html.Div([
            assign_project,
            shift_project
        ], style={"display": "flex"}),
        project_card,
    ]
)





@dash.callback(
    Output("planning_fig_project_planning", "children"),
    [
        Input("projects_planning_year", "value"),
    ]
)
def project_planning(year):

    date = datetime.datetime.today().strftime('%Y-%m-%d')

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
    data = pd.DataFrame(data=data, columns = ["project_id", "fullname", "Start", "Finish", "Task", "Topic"])  # "fullname", 
    data

    fig = sorted_gant(df=data, Task="Task", team_member="fullname", start_date="Start", end_date="Finish", date=date, plot = False)

    return dcc.Graph(figure=fig)



@dash.callback(
    Output("table_projects_planning_overview", "children"),
    [
        Input("projects_planning_year", "value"),
        Input("projects_planning_teammember", "value"),
    ]
    # , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def project_table(year, teammember):

    if teammember != None:
        # SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, pbp.year
        sql=f"""
            
            SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.start_date, p.end_date
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
            WHERE pbp.year = '{year}'
            AND
            tm.team_id in (SELECT team_id FROM team_members WHERE full_name = '{teammember}')
        """


    else:
        # sql=f"""
        #     SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, pbp.year
        #     FROM project p
        #     INNER JOIN founding_sources fs
        #     ON p.funding_id = fs.founding_source_id
        #     INNER JOIN topic_class tc
        #     ON p.topic_class_id = tc.topic_class_id
        #     INNER JOIN project_team_members ptm
        #     ON p.project_id = ptm.project_id
        #     INNER JOIN team_members tm
        #     ON tm.team_id = ptm.team_id
        #     INNER JOIN project_budget_planning pbp
        #     ON pbp.project_id = p.project_id
        #     WHERE pbp.year = '{year}'
        # """
        year_max = str(year)+"-12-30"
        year_min= str(year)+"-01-01"

        sql=f"""
            SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.start_date, p.end_date
            FROM project p
            INNER JOIN founding_sources fs
            ON p.funding_id = fs.founding_source_id
            INNER JOIN topic_class tc
            ON p.topic_class_id = tc.topic_class_id
            LEFT JOIN project_team_members ptm
            ON p.project_id = ptm.project_id
            INNER JOIN project_budget_planning pbp
            ON pbp.project_id = p.project_id
            WHERE p.end_date <= '{year_max}'
            AND
            ptm.team_id IS NULL
            OR
            p.start_date >= '{year_min}'
            AND
            ptm.team_id IS NULL
        """
    data=execute_sql(sql)

    data = pd.DataFrame(data, columns=["project_id", "Topic", "Topic_Class", "Founding Source", "Start", "End"])

    data = data.sort_values(by="project_id")

    data = data.drop_duplicates(keep="first")

    data = data.reset_index(drop=True)

    df_projects = dash_table.DataTable(
        id = "planning_projects_table",
        columns=[{"name": str(i), "id": str(i)} for i in data.columns],
        data=data.to_dict("records"),
        style_table={"height": "300px", "overflow": "auto", "width": "1400px"},
        style_as_list_view=False,
        style_header={"fontweight": "bold", "font-family": "sans-serif"},
        style_cell={
            "font-family": "sans-serif", 
            'overflow': 'hidden',
            "minWidth": 60,
            'textAlign': 'center'
            },
        row_selectable="single",
    )

    return df_projects



# figure callback
@dash.callback(
    Output("fig_project_planning_timeline", "children"),
    [
        Input("projects_planning_year", "value"),
        Input("projects_planning_teammember", "value"),
    ]
)
def create_gant_fig(year, teammember):

    if teammember != None:
        # SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, pbp.year
        sql=f"""
            
            SELECT p.project_id, tm.full_name, p.topic, tc.topic_class, fs.founding_source, p.start_date, p.end_date
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
            WHERE pbp.year = '{year}'
            AND
            tm.team_id in (SELECT team_id FROM team_members WHERE full_name = '{teammember}')
        """

        data=execute_sql(sql)

        data = pd.DataFrame(data, columns=["project_id", "fullname", "Task", "Topic", "Founding Source", "Start", "Finish"])

        data = data.sort_values(by="project_id")

        data = data[data["fullname"] == teammember]

        data = data.sort_values(by="project_id", ascending=False)
        data = data.reset_index(drop = True)

        fig = single_gantt(df=data, team_member=teammember, color="Task", Task="Task", Start="Start", Finish="Finish", date=None, plot = False)

    else:
        year_max = str(year)+"-12-30"
        year_min= str(year)+"-01-01"

        sql=f"""
            SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.start_date, p.end_date
            FROM project p
            INNER JOIN founding_sources fs
            ON p.funding_id = fs.founding_source_id
            INNER JOIN topic_class tc
            ON p.topic_class_id = tc.topic_class_id
            LEFT JOIN project_team_members ptm
            ON p.project_id = ptm.project_id
            INNER JOIN project_budget_planning pbp
            ON pbp.project_id = p.project_id
            WHERE p.end_date <= '{year_max}'
            AND
            ptm.team_id IS NULL
            OR
            p.start_date >= '{year_min}'
            AND
            ptm.team_id IS NULL
        """

        data=execute_sql(sql)

        data = pd.DataFrame(data, columns=["project_id", "Task", "Topic", "Founding Source", "Start", "Finish"])

        data = data.sort_values(by="project_id")

        data = data.sort_values(by="project_id", ascending=False)
        data = data.reset_index(drop = True)

        fig = single_gantt(df=data, team_member=None, color="Task", Task="Task", Start="Start", Finish="Finish", date=None, plot = False)

    return dcc.Graph(figure=fig)
















