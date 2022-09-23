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


# project_id from projects
sql= "SELECT project_id FROM project"
data=execute_sql(sql)

data=pd.DataFrame(data, columns=["project_id"])
list_data=list(data["project_id"])
list_data.sort()
project_options = get_option_list(list_data)


# founding_sources
sql= "SELECT founding_source FROM founding_sources"
data = execute_sql(sql)
data=pd.DataFrame(data, columns=["founding_source"])
list_data=list(data["founding_source"])
list_data.sort()
founding_sources_options = get_option_list(list_data)


# topic_class: topics
sql = """
    SELECT topic_class FROM topic_class
"""
data = execute_sql(sql)
data=pd.DataFrame(data, columns=["topic_class"])
list_data=list(data["topic_class"])
# list_data.sort()
topic_class_options = get_option_list(list_data)



# teammembers: fullname Dropdown
sql = """
    SELECT full_name FROM team_members
"""
data = execute_sql(sql)
data=pd.DataFrame(data, columns=["full_name"])
list_data=list(data["full_name"])
list_data.sort()
team_members_options = get_option_list(list_data)


# difficulty options
option_difficultiy=get_option_list([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# project status options
project_status=get_option_list(["Planned", "Approved", "Ongoing", "Completed", "Rejected"])




# what is this year when loading
this_year=datetime.today().year



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
                small_icon_card(id="projects_add_project", icon="add", color="white"),
                small_icon_card(id="projects_update_project", icon="update", color="white"),
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
                        html.Div(dcc.Textarea(id="new_text", style={"width": "600px", "height": "200px"}))
                    ]
                ),
                content_card_size(
                    id="sub_card2",
                    title="Projects Targets and Goals",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Textarea(id="new_target", style={"width": "600px", "height": "200px"}))
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
                    id="sub_card5",
                    title="Project Budget",
                    size="400px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Loading(id="table_yearly_budget"))
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


assigned_team = content_card_size(
    id="assign_project_content",
    title="Assigned team members",
    size="500px", 
    height="200px",
    content=[
        html.Div(dcc.Loading(id="table_assigned_team"))
    ]
)


assign_project = content_card_size(
    id="assigned_team",
    title="Assign a Project to Team Members",
    size="500px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Team_Member", a_function=dcc.Dropdown(id="single_teammember", options = team_members_options, style={"width": "130px"})),
                small_icon_card(id="projects_assign_team_add_button", icon="add", color="white"),
                small_icon_card(id="projects_assign_team_delete_button", icon="delete", color="white"),
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
                mini_card("Deadline Date", a_function=dcc.DatePickerSingle(id="deadline_date", style={"width": "130px"})),
                mini_card("Deadline Topic", a_function=dcc.Input(id="deadline_topic", type="text", style={"width": "130px"})),
                small_icon_card(id="projects_add_deadline_button", icon="add", color="white"),
                small_icon_card(id="projects_delete_deadline_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


add_yearly_budget = content_card_size(
    id="yearly_budget_content",
    title="Add yearly budget to a project",
    size="800px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Year", a_function=dcc.Input(id="budget_year", type="number", step=1, value=this_year, style={"width": "130px"})),
                mini_card("Budget", a_function=dcc.Input(id="yearly_budget", type="number", min=0, style={"width": "130px"})),
                small_icon_card(id="projects_add_budget_button", icon="add", color="white"),
                small_icon_card(id="projects_update_budget_button", icon="update", color="white"),
                small_icon_card(id="projects_delete_budget_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


assign_yearly_budget_team = content_card_size(
    id="yearly_team_budget",
    title="Assign part of total Budget to Team member",
    size="1000px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Team_Member", a_function=dcc.Dropdown(id="yearly_single_teammember", options = team_members_options, style={"width": "130px"})),
                mini_card("Year", a_function=dcc.Input(id="budget_team_year", type="number", step=1, value=this_year, style={"width": "130px"})),
                mini_card("Budget", a_function=dcc.Input(id="yearly_team_budget", type="number", min=0, style={"width": "130px"})),
                small_icon_card(id="projects_add_team_budget_button", icon="add", color="white"),
                small_icon_card(id="projects_update_team_budget_button", icon="update", color="white"),
                small_icon_card(id="projects_delete_team_budget_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


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
                            id="projects_year", 
                            )
                        ),
                    mini_card("Team Member", 
                        a_function=dcc.Dropdown(
                            id="projects_teammember", 
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
                        dcc.Loading(id="table_projects_overview")
                    ]
                )
            ],
            style={"display": "block"}
        ),
    ]
)

callback_timer = dcc.Interval(id ="update_timer",  interval = 4*1000)  #1000 ms * 4 = 4sec



layout = html.Div(
    children=[

        aproject_card,
        html.Div(
            children=[
                assign_project,
                assigned_team,
            ],
            style={"display": "flex"}
        ),
        add_deadline,
        html.Div(
            children=[
                add_yearly_budget,
            ],
            style={"display": "flex"}
        ),
        assign_yearly_budget_team,
        table_card,
        callback_timer
    ],
    style={"display": "block"}
)





# make the callbacks


# add project
@dash.callback(
    Output("projects_add_project_button", "style"),
    [
        Input("projects_add_project", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_add_project_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_add_project(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id


    if ((button_id == "projects_add_project") and (style['background-color'] == "white") and (style != None)):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    elif ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color



# update project
@dash.callback(
    Output("projects_update_project_button", "style"),
    [
        Input("projects_update_project", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_update_project_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_update_project(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id



    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_update_project"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color




# small_icon_card(id="projects_assign_team_add_button", icon="add", color="white"),
# Assign Team to project
@dash.callback(
    Output("projects_assign_team_add_button_button", "style"),
    [
        Input("projects_assign_team_add_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_assign_team_add_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_assign_team_add(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_assign_team_add_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# small_icon_card(id="projects_assign_team_delete_button", icon="delete", color="white"),
# remove assiged team member from project
@dash.callback(
    Output("projects_assign_team_delete_button_button", "style"),
    [
        Input("projects_assign_team_delete_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_assign_team_delete_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_button_style(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_assign_team_delete_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color







# small_icon_card(id="projects_add_deadline_button", icon="add", color="white"),
# add project deadline
@dash.callback(
    Output("projects_add_deadline_button_button", "style"),
    [
        Input("projects_add_deadline_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_add_deadline_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_add_deadline(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_add_deadline_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color





# small_icon_card(id="projects_delete_deadline_button", icon="delete", color="white"),
# projects_remove_deadline
@dash.callback(
    Output("projects_delete_deadline_button_button", "style"),
    [
        Input("projects_delete_deadline_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_delete_deadline_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_remove_deadline(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_delete_deadline_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color





# small_icon_card(id="projects_add_budget_button", icon="add", color="white"),
# add yearly budget to project
@dash.callback(
    Output("projects_add_budget_button_button", "style"),
    [
        Input("projects_add_budget_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_add_budget_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_add_budget(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_add_budget_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# small_icon_card(id="projects_update_budget_button", icon="update", color="white"),
# update yearly budget
@dash.callback(
    Output("projects_update_budget_button_button", "style"),
    [
        Input("projects_update_budget_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_update_budget_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_update_budget(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_update_budget_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# small_icon_card(id="projects_delete_budget_button", icon="delete", color="white"),
# delete budget
@dash.callback(
    Output("projects_delete_budget_button_button", "style"),
    [
        Input("projects_delete_budget_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_delete_budget_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_delete_budget(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_delete_budget_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color

# small_icon_card(id="projects_add_team_budget_button", icon="add", color="white"),
# budget to some project team members
@dash.callback(
    Output("projects_add_team_budget_button_button", "style"),
    [
        Input("projects_add_team_budget_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_add_team_budget_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_add_budget_to_team(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_add_team_budget_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# small_icon_card(id="projects_update_team_budget_button", icon="update", color="white"),
# update budget to team
@dash.callback(
    Output("projects_update_team_budget_button_button", "style"),
    [
        Input("projects_update_team_budget_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_update_team_budget_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_update_budget_to_team(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_update_team_budget_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# small_icon_card(id="projects_delete_team_budget_button", icon="delete", color="white"),
# delete budget for team
@dash.callback(
    Output("projects_delete_team_budget_button_button", "style"),
    [
        Input("projects_delete_team_budget_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_delete_team_budget_button_button", "style")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_delete_budget_to_team(
    n_clicks, 
    n_interval, 
    style
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_delete_team_budget_button"):
        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color



# @dash.callback(
#     [
#         Output("new_projectid", "options"),
#         Output("new_projectid", "value"),
#     ],
#     [
#         Input("add_project_button", "n_clicks"),
#         State("new_funding", "value"),
#         State("new_topic", "value"),
#         State("new_topic_class", "value"),
#         State("new_argus", "value"),
#         State("new_charging", "value"),
#         State("rec_account", "value"),
#         State("new_account_responsible", "value"),
#         State("new_start", "date"),
#         State("new_end", "date"),
#         State("new_project_diff", "value"),
#         State("new_project_status", "value"),
#         State("new_text", "value"),
#         State("new_target", "value")
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def new_project(n_clicks, funding, topic, topic_class, argus, charging, rec_account, account_resp, start, end, difficulty, status, description, target):

#     if ((funding != None) and (topic != None) and (topic_class != None) and (argus != None) and (charging != None) and(rec_account != None) and (account_resp != None) and (start != None) and (end != None) and (status != None)):

#         sql = f"""
#             INSERT INTO project (funding_id, topic, topic_class_id, argus_enabled, way_charging, recieving_account, cost_center_respon, start_date, end_date, difficulty, project_status, project_description, project_goals) VALUES 
#             (
#                 (SELECT founding_source_id FROM founding_sources WHERE founding_source = '{funding}'),
#                 '{topic}',
#                 (SELECT topic_class_id FROM topic_class WHERE topic_class = '{topic_class}'),
#                 '{argus}',
#                 '{charging}',
#                 '{rec_account}',
#                 '{account_resp}',
#                 '{start}',
#                 '{end}',
#                 '{difficulty}',
#                 '{status}',
#                 '{description}',
#                 '{target}'
#             );
#         """

#         data = execute_sql(sql)

#     sql= "SELECT project_id FROM project"
#     data=execute_sql(sql)

#     data=pd.DataFrame(data, columns=["project_id"])
#     list_data=list(data["project_id"])
#     list_data.sort()
#     project_options = get_option_list(list_data)

#     sql = f"SELECT project_id FROM project WHERE topic = '{topic}';"
#     new_index = execute_sql(sql)[0][0]

#     return project_options, new_index



# @dash.callback(
#     [
#         Output("new_funding", "value"),
#         Output("new_topic", "value"),
#         Output("new_topic_class", "value"),
#         Output("new_argus", "value"),
#         Output("new_charging", "value"),
#         Output("rec_account", "value"),
#         Output("new_account_responsible", "value"),
#         Output("new_start", "date"),
#         Output("new_end", "date"),
#         Output("new_project_diff", "value"),
#         Output("new_project_status", "value"),
#         Output("new_text", "value"),
#         Output("new_target", "value")
#     ],
#     [
#         Input("new_projectid", "value"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def load_project(project_id):

#     if project_id != None:

#         sql = f"""
#             SELECT fs.founding_source, p.topic, tc.topic_class, p.argus_enabled, p.way_charging, p.recieving_account, p.cost_center_respon, p.start_date, p.end_date, p.difficulty, p.project_status, p.project_description, p.project_goals
#             FROM project p
#             INNER JOIN topic_class tc
#             ON p.topic_class_id = tc.topic_class_id
#             INNER JOIN founding_sources fs
#             ON p.funding_id = fs.founding_source_id
#             WHERE p.project_id = '{project_id}';
#         """

#         data = execute_sql(sql)

#         data = pd.DataFrame(data, columns=["funding", "topic", "topic_class", "argus", "charging", "rec_account", "account_resp", "start", "end", "difficulty", "status", "description", "target"])

#         funding = data.loc[0, "funding"]
#         topic = data.loc[0, "topic"]
#         topic_class = data.loc[0, "topic_class"]
#         argus = data.loc[0, "argus"]
#         charging = data.loc[0, "charging"]
#         rec_account = data.loc[0, "rec_account"]
#         account_resp = data.loc[0, "account_resp"]
#         start = data.loc[0, "start"]
#         end = data.loc[0, "end"]
#         difficulty = data.loc[0, "difficulty"]
#         status = data.loc[0, "status"]
#         description = data.loc[0, "description"]
#         target = data.loc[0, "target"]
    
#     else:
#         funding = topic = topic_class = argus = charging = rec_account = account_resp = start = end = difficulty = status = description = target = None

#     return funding, topic, topic_class, argus, charging, rec_account, account_resp, start, end, difficulty, status, description, target



# @dash.callback(
#     [
#         Output("budget_year", "min"),
#         Output("budget_year", "max")
#     ],
#     [
#         Input("new_start", "date"),
#         Input("new_end", "date")
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def update_budget_year_limits(start_date, end_date):

#     year_low = datetime.strptime(start_date, "%Y-%m-%d")
#     year_high = datetime.strptime(end_date, "%Y-%m-%d")

#     return year_low.year, year_high.year




# @dash.callback(
#     Output("update_project", "style"),
#     [
#         Input("update_project_button", "n_clicks"),
#         State("new_projectid", "value"),
#         State("new_funding", "value"),
#         State("new_topic", "value"),
#         State("new_topic_class", "value"),
#         State("new_argus", "value"),
#         State("new_charging", "value"),
#         State("rec_account", "value"),
#         State("new_account_responsible", "value"),
#         State("new_start", "date"),
#         State("new_end", "date"),
#         State("new_project_diff", "value"),
#         State("new_project_status", "value"),
#         State("new_text", "value"),
#         State("new_target", "value")
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def update_project(n_clicks, project_id, funding, topic, topic_class, argus, charging, rec_account, account_resp, start, end, difficulty, status, description, target):

#     sql = f"""
#         UPDATE project
#         SET
#         funding_id = (SELECT founding_source_id FROM founding_sources WHERE founding_source = '{funding}'),
#         topic = '{topic}',
#         topic_class_id = (SELECT topic_class_id FROM topic_class WHERE topic_class = '{topic_class}'),
#         argus_enabled = '{argus}',
#         way_charging = '{charging}',
#         recieving_account = '{rec_account}',
#         cost_center_respon = '{account_resp}',
#         start_date = '{start}',
#         end_date = '{end}',
#         difficulty = '{difficulty}',
#         project_status = '{status}',
#         project_description = '{description}',
#         project_goals = '{target}'
#         WHERE project_id = '{project_id}';
#     """
#     data = execute_sql(sql)
#     data

#     color = {"background-color": "white"}

#     return color


# @dash.callback(
#     Output("add_button", "style"),
#     [
#         Input("update_project_button", "n_clicks"),
#         Input("add_button_button", "n_clicks"),
#         Input("new_projectid", "value"),
#         State("single_teammember", "value"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def update_project_teammember(update_button, add_button, project_id, teammember):

#     if ((project_id != None) and (teammember != None)):

#         sql = f"""
#             INSERT INTO project_team_members(project_id, team_id) VALUES
#             (
#                 (SELECT project_id FROM project WHERE project_id = '{project_id}'),
#                 (SELECT team_id FROM team_members WHERE full_name = '{teammember}')
#             )
#         """
#         execute_sql(sql)

#     color = {"background-color": "white"}

#     return color


# @dash.callback(
#     Output("delete_button", "style"),
#     [
#         Input("delete_button_button", "n_clicks"),
#         Input("new_projectid", "value"),
#         State("single_teammember", "value"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def delete_project_teammember(delete_button, project_id, teammember):

#     if ((project_id != None) and (teammember != None)):

#         sql = f"""
#             DELETE FROM project_team_members
#             WHERE
#             project_id in (SELECT project_id FROM project WHERE project_id = '{project_id}')
#             AND
#             team_id in (SELECT team_id FROM team_members WHERE full_name = '{teammember}');
#         """
#         execute_sql(sql)

#     color = {"background-color": "white"}

#     return color


# @dash.callback(
#     Output("table_team", "children"),
#     [
#         Input("update_project_button", "n_clicks"),
#         Input("add_button_button", "n_clicks"),
#         Input("delete_button_button", "n_clicks"),
#         Input("new_projectid", "value"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def update_project_teammember_table(update_button, add_button, delete_button, project_id):

#     if (project_id != None):

#         sleep(1)

#         sql = f"""
#             SELECT tm.full_name
#             FROM team_members tm
#             INNER JOIN project_team_members ptm
#             ON ptm.team_id = tm.team_id
#             INNER JOIN project p
#             ON p.project_id = ptm.project_id
#             WHERE p.project_id = '{project_id}'
#             """

#         data = execute_sql(sql)

#         data = pd.DataFrame(data, columns=["active PrAI Team members"])

#         df_team = dash_table.DataTable(
#             id = "table_teammembers",
#             columns=[{"name": str(i), "id": str(i)} for i in data.columns],
#             data=data.to_dict("records"),
#             style_table={"height": "200px", "overflow": "auto", "width": "300px"},
#             style_as_list_view=True,
#             style_header={"fontweight": "bold", "font-family": "sans-serif"},
#             style_cell={
#                 "font-family": "sans-serif", 
#                 'overflow': 'hidden',
#                 "minWidth": 60
#                 },
#             row_selectable=False,
#         )
#     else: 
#         df_team = None

#     return df_team


# @dash.callback(

#     Output("table_deadlines", "children"),
#     [
#         Input("new_projectid", "value"),
#         Input("add_deadline_button", "n_clicks"),
#         Input("update_project_button", "n_clicks"),
#         Input("delete_deadline_button", "n_clicks"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def update_project_deadlines_table(project_id, deadline_button, update_project_button, delete_deadline_button):

#     if (project_id != None):

#         sleep(1)

#         sql = f"""
#             SELECT deadline_date, deadline_text FROM project_deadlines
#             WHERE project_id = {project_id}
#             """
#         data=execute_sql(sql)

#         data = pd.DataFrame(data, columns=["Date", "Topic"])

#         data = data.sort_values(by="Date")

#         df_deadline = dash_table.DataTable(
#             id = "deadlines_table",
#             columns=[{"name": str(i), "id": str(i)} for i in data.columns],
#             data=data.to_dict("records"),
#             style_table={"height": "200px", "overflow": "auto", "width": "400px"},
#             style_as_list_view=True,
#             style_header={"fontweight": "bold", "font-family": "sans-serif"},
#             style_cell={
#                 "font-family": "sans-serif", 
#                 'overflow': 'hidden',
#                 "minWidth": 60
#                 },
#             row_selectable="single",
#         )

#     else: 
#         df_deadline = None

#     return df_deadline





# @dash.callback(
#     Output("add_deadline_button", "style"),
#     [
#         Input("add_deadline_button", "n_clicks"),
#         State("deadline_date", "date"),
#         State("deadline_topic", "value"),
#         State("new_projectid", "value"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def update_deadlines_table(add_button, deadline_date, deadline_topic, project_id):

#     if ((deadline_date != None) and (deadline_topic != None) and (project_id != None)):

#         sql = f"""
#             INSERT INTO project_deadlines(project_id, deadline_date, deadline_text) VALUES
#             (
#                 (SELECT project_id FROM project WHERE project_id = '{project_id}'),
#                 '{deadline_date}',
#                 '{deadline_topic}'
#             );
#         """
#         data = execute_sql(sql)
#         data

#     color = {"background-color": "white"}

#     return color


# @dash.callback(
#     Output("delete_deadline_button", "style"),
#     [
#         Input("delete_deadline_button", "n_clicks"),
#         State("deadline_date", "date"),
#         State("deadline_topic", "value"),
#         State("new_projectid", "value"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def remove_deadlines_table(button, deadline_date, deadline_topic, project_id):

#     if ((deadline_date != None) and (deadline_topic != None) and (project_id != None)):

#         sql = f"""

#             DELETE FROM project_deadlines
#             WHERE
#             project_id in (SELECT project_id FROM project WHERE project_id = '{project_id}')
#             AND
#             deadline_date = '{deadline_date}'
#             AND
#             deadline_text = '{deadline_topic}';
#         """
#         data = execute_sql(sql)
#         data

#     color = {"background-color": "white"}

#     return color




# @dash.callback(
#     [
#         Output("deadline_date", "date"),
#         Output("deadline_topic", "value")
#     ],
#     [
#         Input("deadlines_table", "selected_rows"),
#         Input("deadlines_table", "data"),
#         State("new_projectid", "value"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def select_table(selected_row, raw_data, projectid):

#     if ((projectid != None) and (raw_data != None) and (selected_row != None)):

#         data = pd.DataFrame(raw_data, columns=["Date", "Topic"])

#         date = list(set(data.loc[selected_row, "Date"]))[0]
#         topic = list(set(data.loc[selected_row, "Topic"]))[0]
#     else:
#         date = topic = None

#     return date, topic



# @dash.callback(

#     Output("table_projects_overview", "children"),
#     [
#         Input("update_project_button", "n_clicks"),
#         Input("add_button_button", "n_clicks"),
#         Input("new_projectid", "value")
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def update_project_table(update_project_button, add_project_button, project_id_value):

#     sql="""
#         SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.project_description
#         FROM project p
#         INNER JOIN founding_sources fs
#         ON p.funding_id = fs.founding_source_id
#         INNER JOIN topic_class tc
#         ON p.topic_class_id = tc.topic_class_id
#     """
#     data=execute_sql(sql)

#     data = pd.DataFrame(data, columns=["project_id", "Topic", "Topic_Class", "Founding Source", "Project Desc."])

#     data = data.sort_values(by="project_id")

#     df_projects = dash_table.DataTable(
#         id = "projects_table",
#         columns=[{"name": str(i), "id": str(i)} for i in data.columns],
#         data=data.to_dict("records"),
#         style_table={"height": "400px", "overflow": "auto", "width": "1300px"},
#         style_as_list_view=True,
#         style_header={"fontweight": "bold", "font-family": "sans-serif"},
#         style_cell={
#             "font-family": "sans-serif", 
#             'overflow': 'hidden',
#             "minWidth": 60
#             },
#         row_selectable="single",
#     )

#     return df_projects




# @dash.callback(

#     Output("table_yearly_budget", "children"),
#     [
#         Input("new_projectid", "value"),
#         Input("add_budget_button", "n_clicks"),
#         Input("update_budget_button", "n_clicks"),
#         Input("delete_budget_button", "n_clicks")
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def update_project_budget_table(project_id, add_budget_button, update_budget_button, delete_budget_button):

#     if project_id != None:

#         sleep(0.1)

#         sql=f"""
#             SELECT pbp.year, pbp.budget
#             FROM project_budget_planning pbp
#             WHERE project_id = {project_id}
#         """
#         data=execute_sql(sql)

#         data = pd.DataFrame(data, columns=["Year", "Budget"])

#         data = data.sort_values(by="Year")

#         df_budget_table = dash_table.DataTable(
#             id = "project_budget_table",
#             columns=[{"name": str(i), "id": str(i)} for i in data.columns],
#             data=data.to_dict("records"),
#             style_table={"height": "400px", "overflow": "auto", "width": "300px"},
#             style_as_list_view=True,
#             style_header={"fontweight": "bold", "font-family": "sans-serif"},
#             style_cell={
#                 "font-family": "sans-serif", 
#                 'overflow': 'hidden',
#                 "minWidth": 60
#                 },
#             row_selectable=False,
#         )
    
#     else:
#         df_budget_table = None

#     return df_budget_table




# @dash.callback(
#     Output("add_budget_button", "style"),
#     [
#         Input("add_budget_button", "n_clicks"),
#         State("new_projectid", "value"),
#         State("budget_year", "value"),
#         State("yearly_budget", "value")
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def add_project_budget(add_budget_button, project_id, budget_year, yearly_budget):

#     if ((project_id != None) and (budget_year != None) and (yearly_budget != None)):

#         sql = f"""
#             INSERT INTO project_budget_planning (project_id, year, budget) VALUES
#             (
#                 (SELECT project_id FROM project WHERE project_id = '{project_id}'),
#                 '{budget_year}',
#                 '{yearly_budget}'
#             );
#         """

#         data=execute_sql(sql)

#         color = {"background-color": "white"}

#         return color



# @dash.callback(
#     Output("delete_budget_button", "style"),
#     [
#         Input("delete_budget_button", "n_clicks"),
#         State("new_projectid", "value"),
#         State("budget_year", "value"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def delete_project_budget(delete_budget_button, project_id, budget_year):

#     if ((project_id != None) and (budget_year != None)):

#         sql = f"""
#         DELETE FROM project_budget_planning
#         WHERE
#         project_id in (SELECT project_id FROM project WHERE project_id = '{project_id}')
#         AND
#         year = '{budget_year}';
#         """

#         data=execute_sql(sql)

#         color = {"background-color": "white"}

#         return color




# @dash.callback(
#     Output("update_budget_button", "style"),
#     [
#         Input("update_budget_button", "n_clicks"),
#         State("new_projectid", "value"),
#         State("budget_year", "value"),
#         State("yearly_budget", "value"),
#     ]
#     , prevent_initial_call=True
#     , suppress_callback_exceptions=True
# )
# def update_project_budget(delete_budget_button, project_id, budget_year, yearly_budget, teammember):

#     if ((project_id != None) and (budget_year != None)):

#         sql = f"""
#             UPDATE project_budget_planning
#             SET
#             project_id = (SELECT project_id FROM project WHERE project_id = '{project_id}'),
#             year = '{budget_year}',
#             budget = '{yearly_budget}'
#             WHERE project_id = '{project_id}' 
#             AND year = '{budget_year}';
#         """
#         execute_sql(sql)

#         color = {"background-color": "white"}

#         return color


