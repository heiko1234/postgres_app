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



sql= "SELECT project_id FROM project"
data=execute_sql(sql)

data=pd.DataFrame(data, columns=["project_id"])
list_data=list(data["project_id"])
list_data.sort()
project_options = get_option_list(list_data)


sql= "SELECT founding_source FROM founding_sources"
data = execute_sql(sql)
data=pd.DataFrame(data, columns=["founding_source"])
list_data=list(data["founding_source"])
list_data.sort()
founding_sources_options = get_option_list(list_data)


sql = """
    SELECT topic_class FROM topic_class
"""
data = execute_sql(sql)
data=pd.DataFrame(data, columns=["topic_class"])
list_data=list(data["topic_class"])
# list_data.sort()
topic_class_options = get_option_list(list_data)

option_difficultiy=get_option_list([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
project_status=get_option_list(["Planned", "Approved", "Ongoing", "Completed", "Rejected"])

# dcc.Dropdown(id="i_entity", options=entity_options, style={"width": "130px"})),



# what is this year when loading
this_year=datetime.datetime.today().year



aproject_card = content_card_size(
    id="project_content",
    title="Project",
    size="1420px", 
    height="900px",
    content=[
        html.Div(
            children=[
                mini_card("Project_ID", a_function=dcc.Dropdown(id="new_projectid", options=project_options, style={"width": "130px"})),
                mini_card("Funding", a_function=dcc.Dropdown(id="new_funding", options=founding_sources_options, style={"width": "130px"})),
                mini_card("Topic", a_function=dcc.Input(id="new_topic", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Topic Class", a_function=dcc.Dropdown(id="new_topic_class", options=topic_class_options, style={"width": "130px"})),
                mini_card("Argus enabled", a_function=dcc.Dropdown(id="new_argus", value="Yes", options=[{"label": "Yes", "value": "Yes"}, {"label": "No", "value": "No"}], style={"width": "130px"})),
                mini_card("Way of charging", a_function=dcc.Dropdown(id="new_charging", value="Manual", options=[{"label": "Manual", "value": "Manual"}, {"label": "LRM", "value": "LRM"}], style={"width": "130px"})),
                small_icon_card(id="add_project", icon="add", color="white"),
                small_icon_card(id="update_project", icon="update", color="white"),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                mini_card("Rec. Account", a_function=dcc.Input(id="rec_account", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Cost Center Resp.", a_function=dcc.Input(id="new_account_responsible", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Start Date", a_function=dcc.DatePickerSingle(id="new_start", style={"width": "130px"})),
                mini_card("End Date", a_function=dcc.DatePickerSingle(id="new_end", style={"width": "130px"})),
                mini_card("Difficulty", a_function=dcc.Dropdown(id="new_project_diff", options=option_difficultiy, value="5", style={"width": "130px"})),
                mini_card("Project Status", a_function=dcc.Dropdown(id="new_project_status", options = project_status, value= "Planned", style={"width": "130px"})),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                content_card_size(
                    id="sub_card",
                    title="Project Description",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Input(id="new_text", type="text", style={"width": "600px", "height": "200px"}))
                    ]
                ),
                content_card_size(
                    id="sub_card2",
                    title="Projects Targets and Goals",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Input(id="new_target", type="text", style={"width": "600px", "height": "200px"}))
                    ]
                ),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                content_card_size(
                    id="sub_card3",
                    title="Project Team",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Loading(id="table_team"))
                    ]
                ),
                content_card_size(
                    id="sub_card4",
                    title="Project Deadlines",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Loading(id="table_deadlines"))
                    ]
                ),
            ],
            style={"display": "flex"}
        )
    ]
)


asign_project = content_card_size(
    id="asign_project_content",
    title="Asign a Project to a team member",
    size="500px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Team_Memeber", a_function=dcc.Input(id="new_teamid", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_button", icon="add", color="white"),
                small_icon_card(id="delete_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)

add_deadline = content_card_size(
    id="deadline_project_content",
    title="Add a deadline",
    size="700px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Deadline Date", a_function=dcc.Input(id="new_deadlineid", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Deadline Topic", a_function=dcc.Input(id="new_topicid", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_button", icon="add", color="white"),
                small_icon_card(id="delete_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)




layout = html.Div(
    children=[

        aproject_card,
        html.Div(
            children=[
                asign_project,
                add_deadline
            ],
            style={"display": "flex"}
        ),
        
    ],
    style={"display": "block"}
)








@dash.callback(
    [
        Output("new_projectid", "options"),
        Output("new_projectid", "value"),
    ],
    [
        Input("add_project_button", "n_clicks"),
        State("new_funding", "value"),
        State("new_topic", "value"),
        State("new_topic_class", "value"),
        State("new_argus", "value"),
        State("new_charging", "value"),
        State("rec_account", "value"),
        State("new_account_responsible", "value"),
        State("new_start", "date"),
        State("new_end", "date"),
        State("new_project_diff", "value"),
        State("new_project_status", "value"),
        State("new_text", "value"),
        State("new_target", "value")
    ]
    ,prevent_initial_call=True
)
def new_project(n_clicks, funding, topic, topic_class, argus, charging, rec_account, account_resp, start, end, difficulty, status, description, target):

    if ((funding != None) and (topic != None) and (topic_class != None) and (argus != None) and (charging != None) and(rec_account != None) and (account_resp != None) and (start != None) and (end != None) and (status != None)):

        sql = f"""
            INSERT INTO project (funding_id, topic, topic_class_id, argus_enabled, way_charging, recieving_account, cost_center_respon, start_date, end_date, difficulty, project_status, project_description, project_goals) VALUES 
            (
                (SELECT founding_source_id FROM founding_sources WHERE founding_source = '{funding}'),
                '{topic}',
                (SELECT topic_class_id FROM topic_class WHERE topic_class = '{topic_class}'),
                '{argus}',
                '{charging}',
                '{rec_account}',
                '{account_resp}',
                '{start}',
                '{end}',
                '{difficulty}',
                '{status}',
                '{description}',
                '{target}'
            );
        """

        data = execute_sql(sql)

    sql= "SELECT project_id FROM project"
    data=execute_sql(sql)

    data=pd.DataFrame(data, columns=["project_id"])
    list_data=list(data["project_id"])
    list_data.sort()
    project_options = get_option_list(list_data)

    sql = f"SELECT project_id FROM project WHERE topic = '{topic}';"
    new_index = execute_sql(sql)[0][0]

    return project_options, new_index



@dash.callback(
    [
        Output("new_funding", "value"),
        Output("new_topic", "value"),
        Output("new_topic_class", "value"),
        Output("new_argus", "value"),
        Output("new_charging", "value"),
        Output("rec_account", "value"),
        Output("new_account_responsible", "value"),
        Output("new_start", "date"),
        Output("new_end", "date"),
        Output("new_project_diff", "value"),
        Output("new_project_status", "value"),
        Output("new_text", "value"),
        Output("new_target", "value")
    ],
    [
        Input("new_projectid", "value"),
    ]
    ,prevent_initial_call=True
)
def load_project(project_id):

    if project_id != None:

        sql = f"""
            SELECT fs.founding_source, p.topic, tc.topic_class, p.argus_enabled, p.way_charging, p.recieving_account, p.cost_center_respon, p.start_date, p.end_date, p.difficulty, p.project_status, p.project_description, p.project_goals
            FROM project p
            INNER JOIN topic_class tc
            ON p.topic_class_id = tc.topic_class_id
            INNER JOIN founding_sources fs
            ON p.funding_id = fs.founding_source_id
            WHERE p.project_id = '{project_id}';
        """

        data = execute_sql(sql)

        data = pd.DataFrame(data, columns=["funding", "topic", "topic_class", "argus", "charging", "rec_account", "account_resp", "start", "end", "difficulty", "status", "description", "target"])


        funding = data.loc[0, "funding"]
        topic = data.loc[0, "topic"]
        topic_class = data.loc[0, "topic_class"]
        argus = data.loc[0, "argus"]
        charging = data.loc[0, "charging"]
        rec_account = data.loc[0, "rec_account"]
        account_resp = data.loc[0, "account_resp"]
        start = data.loc[0, "start"]
        end = data.loc[0, "end"]
        difficulty = data.loc[0, "difficulty"]
        status = data.loc[0, "status"]
        description = data.loc[0, "description"]
        target = data.loc[0, "target"]
    
    else:
        funding = topic = topic_class = argus = charging = rec_account = account_resp = start = end = difficulty = status = description = target = None

    return funding, topic, topic_class, argus, charging, rec_account, account_resp, start, end, difficulty, status, description, target



@dash.callback(
    Output("update_project", "style"),
    [
        Input("update_project_button", "n_clicks"),
        State("new_projectid", "value"),
        State("new_funding", "value"),
        State("new_topic", "value"),
        State("new_topic_class", "value"),
        State("new_argus", "value"),
        State("new_charging", "value"),
        State("rec_account", "value"),
        State("new_account_responsible", "value"),
        State("new_start", "date"),
        State("new_end", "date"),
        State("new_project_diff", "value"),
        State("new_project_status", "value"),
        State("new_text", "value"),
        State("new_target", "value")
    ]
    ,prevent_initial_call=True
)
def update_project(n_clicks, project_id, funding, topic, topic_class, argus, charging, rec_account, account_resp, start, end, difficulty, status, description, target):

    sql = f"""
        UPDATE project
        SET
        funding_id = (SELECT founding_source_id FROM founding_sources WHERE founding_source = '{funding}'),
        topic = '{topic}',
        topic_class_id = (SELECT topic_class_id FROM topic_class WHERE topic_class = '{topic_class}'),
        argus_enabled = '{argus}',
        way_charging = '{charging}',
        recieving_account = '{rec_account}',
        cost_center_respon = '{account_resp}',
        start_date = '{start}',
        end_date = '{end}',
        difficulty = '{difficulty}',
        project_status = '{status}',
        project_description = '{description}',
        project_goals = '{target}'
        WHERE project_id = '{project_id}';
    """
    data = execute_sql(sql)
    data

    color = {"background-color": "white"}

    return color

