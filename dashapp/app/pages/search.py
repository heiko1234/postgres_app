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



# # project_id from projects
sql= "SELECT project_id FROM project"
data=execute_sql(sql)

data=pd.DataFrame(data, columns=["project_id"])
list_data=list(data["project_id"])
list_data.sort(reverse=True)
project_options = get_option_list(list_data)



def create_searchterm(search_string):
    output = ""
    for count, value in enumerate(search_string.split(" ")):
        if count==0:
            output=output+f"(\m{value}\M)"
        else:
            output=output+f"|(\m{value}\M)"
    return output



search_card = content_card_size(
    id="project_search_content",
    title="Search a Project",
    size="1420px", 
    height="500px",
    content=[
        html.Div(
            children=[
                mini_card("Search", a_function=dcc.Input(id="search_text_input", type="text", placeholder="", style={"width": "130px"}))
            ]
        ),
        dcc.Markdown("\n---\n"),
        dcc.Loading(id="load_search_results")
    ]
)


aproject_card = content_card_size(
    id="project_content_planning",
    title="Project",
    size="1420px", 
    height="1200px",
    content=[
        html.Div(
            children=[
                mini_card("Project_ID", a_function=dcc.Dropdown(id="search_projectid", 
                    options=project_options,
                    style={"width": "130px"})),
                mini_card("Funding", a_function=dcc.Textarea(id="search_funding", 
                    style={"width": "130px"})),
                mini_card("Topic", a_function=dcc.Textarea(id="search_topic", style={"width": "130px"})),
                mini_card("Topic Class", a_function=dcc.Textarea(id="search_topic_class", 
                    style={"width": "130px"})),
                mini_card("Argus enabled", a_function=dcc.Textarea(id="search_argus", style={"width": "130px"})),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                mini_card("Way of charging", a_function=dcc.Textarea(id="search_charging",  style={"width": "130px"})),
                mini_card("Cost Center Resp.", a_function=dcc.Textarea(id="search_account_responsible", style={"width": "130px"})),
                mini_card("Start Date", a_function=dcc.DatePickerSingle(id="search_start", disabled=True, style={"width": "130px"})),
                mini_card("End Date", a_function=dcc.DatePickerSingle(id="search_end", disabled=True, style={"width": "130px"})),
                mini_card("Difficulty", a_function=dcc.Textarea(id="search_project_diff", style={"width": "130px"})),
                mini_card("Project Status", a_function=dcc.Textarea(id="search_project_status", style={"width": "130px"})),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                content_card_size(
                    id="search_sub_card",
                    title="Project Description",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Textarea(id="search_text", style={"width": "600px", "height": "200px"}))
                    ]
                ),
                content_card_size(
                    id="search_sub_card2",
                    title="Projects Targets and Goals",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Textarea(id="search_target", style={"width": "600px", "height": "200px"}))
                    ]
                ),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                content_card_size(
                    id="search_sub_card3",
                    title="Project Deadlines",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Loading(id="search_table_deadlines"))
                    ]
                )
            ]
        ),
        html.Div(
            children=[
                content_card_size(
                    id="search_sub_card4",
                    title="Project Team",
                    size="400px", 
                    height="200px",
                    content=[
                        html.Div(dcc.Loading(id="search_table_team"))
                    ]
                ),
                content_card_size(
                    id="search_sub_card5",
                    title="Project Budget",
                    size="400px", 
                    height="200px",
                    content=[
                        html.Div(dcc.Loading(id="search_table_yearly_budget"))
                    ]
                ),
            ],
            style={"display": "flex"}
        )
    ]
)


layout = html.Div(
    children=[
        search_card,
        aproject_card
    ]
)


@dash.callback(
    Output("load_search_results", "children"),
    [
        Input("search_text_input", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def return_search_result(search_string):

    if search_string is not None:

        statement = create_searchterm(search_string)

        sql = f"""
                SELECT p.project_id, p.start_date, p.end_date, p.topic, tc.topic_class
                FROM project p
                INNER JOIN founding_sources fs
                ON p.funding_id = fs.founding_source_id
                INNER JOIN topic_class tc
                ON p.topic_class_id = tc.topic_class_id
                WHERE project_description ~* '{statement}'
                OR
                project_goals ~* '{statement}'
            """

        search_date = execute_sql(sql)

        data = pd.DataFrame(data=search_date, columns = ["project_id", "Start", "Finish", "Task", "Topic"])

    else:
        data = pd.DataFrame()

    df_output = dash_table.DataTable(
        id = "table_search_results",
        columns=[{"name": str(i), "id": str(i)} for i in data.columns],
        data=data.to_dict("records"),
        style_table={"height": "300px", "overflow": "auto", "width": "1400px"},
        style_as_list_view=True,
        style_header={"fontweight": "bold", "font-family": "sans-serif"},
        style_cell={
            "font-family": "sans-serif", 
            'overflow': 'hidden',
            "minWidth": 60
            },
        row_selectable="single",
    )

    return df_output



@dash.callback(
    Output("search_projectid", "value"),
    [
        Input("table_search_results", "selected_rows"),
        Input("table_search_results", "data")
    ]
)
def get_projectid_from_projectstable(selected_row, raw_data):

    mdata = pd.DataFrame(data = raw_data)

    scnames=["project_id", "Start", "Finish", "Task", "Topic"]

    selected_data = mdata.loc[selected_row, scnames]
    selected_data = selected_data.reset_index(drop= True)

    project_id = selected_data.loc[0, "project_id"]

    return project_id


# give values when project id is selected
@dash.callback(
    [
        Output("search_funding", "value"),
        Output("search_topic", "value"),
        Output("search_topic_class", "value"),
        Output("search_argus", "value"),
        Output("search_charging", "value"),
        Output("search_account_responsible", "value"),
        Output("search_start", "date"),
        Output("search_end", "date"),
        Output("search_project_diff", "value"),
        Output("search_project_status", "value"),
        Output("search_text", "value"),
        Output("search_target", "value")
    ],
    [
        Input("search_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def load_project(project_id):

    if project_id != None:

        sql = f"""
            SELECT fs.founding_source, p.topic, tc.topic_class, p.argus_enabled, p.way_charging, p.cost_center_respon, p.start_date, p.end_date, p.difficulty, p.project_status, p.project_description, p.project_goals
            FROM project p
            INNER JOIN topic_class tc
            ON p.topic_class_id = tc.topic_class_id
            INNER JOIN founding_sources fs
            ON p.funding_id = fs.founding_source_id
            WHERE p.project_id = '{project_id}';
        """

        data = execute_sql(sql)

        data = pd.DataFrame(data, columns=["funding", "topic", "topic_class", "argus", "charging", "account_resp", "start", "end", "difficulty", "status", "description", "target"])
        # print(data)

        funding = data.loc[0, "funding"]
        topic = data.loc[0, "topic"]
        topic_class = data.loc[0, "topic_class"]
        argus = data.loc[0, "argus"]
        charging = data.loc[0, "charging"]
        account_resp = data.loc[0, "account_resp"]

        start = data.loc[0, "start"]
        end = data.loc[0, "end"]

        difficulty = str(data.loc[0, "difficulty"])
        status = data.loc[0, "status"]
        description = data.loc[0, "description"]
        target = data.loc[0, "target"]
    
    else:
        funding = topic = topic_class = argus = charging =  account_resp = start = end = difficulty = status = description = target = None

    return funding, topic, topic_class, argus, charging, account_resp, start, end, difficulty, status, description, target


# update and create deadline tables
@dash.callback(

    Output("search_table_deadlines", "children"),
    [
        Input("search_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def project_deadlines_table(project_id):

    if (project_id != None):

        sleep(1)

        sql = f"""
            SELECT deadline_date, deadline_text FROM project_deadlines
            WHERE project_id = {project_id}
            """
        data=execute_sql(sql)

        data = pd.DataFrame(data, columns=["Date", "Topic"])

        data = data.sort_values(by="Date")

        df_deadline = dash_table.DataTable(
            id = "search_deadlines_table",
            columns=[{"name": str(i), "id": str(i)} for i in data.columns],
            data=data.to_dict("records"),
            style_table={"height": "200px", "overflow": "auto", "width": "400px"},
            style_as_list_view=True,
            style_header={"fontweight": "bold", "font-family": "sans-serif"},
            style_cell={
                "font-family": "sans-serif", 
                'overflow': 'hidden',
                "minWidth": 60
                },
            row_selectable="single",
        )

    else: 
        df_deadline = None

    return df_deadline




# show up teammember_table
@dash.callback(
    Output("search_table_team", "children"),
    [
        Input("search_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def project_teammember_table(project_id):

    if (project_id != None):

        sleep(1)

        sql = f"""
            SELECT tm.full_name
            FROM team_members tm
            INNER JOIN project_team_members ptm
            ON ptm.team_id = tm.team_id
            INNER JOIN project p
            ON p.project_id = ptm.project_id
            WHERE p.project_id = '{project_id}'
            """

        data = execute_sql(sql)

        data = pd.DataFrame(data, columns=["active PrAI Team members"])

        df_team = dash_table.DataTable(
            id = "search_table_teammembers",
            columns=[{"name": str(i), "id": str(i)} for i in data.columns],
            data=data.to_dict("records"),
            style_table={"height": "200px", "overflow": "auto", "width": "300px"},
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
        df_team = None

    return df_team


# show update project budget table
@dash.callback(

    Output("search_table_yearly_budget", "children"),
    [
        Input("search_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def project_budget_table(project_id):

    if project_id != None:

        sleep(0.1)

        sql=f"""
            SELECT pbp.year, pbp.budget
            FROM project_budget_planning pbp
            WHERE project_id = {project_id}
        """
        data=execute_sql(sql)

        data = pd.DataFrame(data, columns=["Year", "Budget"])

        data = data.sort_values(by="Year")

        df_budget_table = dash_table.DataTable(
            id = "search_project_budget_table",
            columns=[{"name": str(i), "id": str(i)} for i in data.columns],
            data=data.to_dict("records"),
            style_table={"height": "150px", "overflow": "auto", "width": "300px"},
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
        df_budget_table = None

    return df_budget_table







