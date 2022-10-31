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


# project_id from projects
# sql= "SELECT project_id FROM project"
# data=execute_sql(sql)

# data=pd.DataFrame(data, columns=["project_id"])
# list_data=list(data["project_id"])
# list_data.sort()
# project_options = get_option_list(list_data)


# founding_sources
# sql= "SELECT founding_source FROM founding_sources"
# data = execute_sql(sql)
# data=pd.DataFrame(data, columns=["founding_source"])
# list_data=list(data["founding_source"])
# list_data.sort()
# founding_sources_options = get_option_list(list_data)


# topic_class: topics
# sql = """
#     SELECT topic_class FROM topic_class
# """
# data = execute_sql(sql)
# data=pd.DataFrame(data, columns=["topic_class"])
# list_data=list(data["topic_class"])
# # list_data.sort()
# topic_class_options = get_option_list(list_data)



# teammembers: fullname Dropdown
# sql = """
#     SELECT full_name FROM team_members
# """
# data = execute_sql(sql)
# data=pd.DataFrame(data, columns=["full_name"])
# list_data=list(data["full_name"])
# list_data.sort()
# team_members_options = get_option_list(list_data)


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
    height="1200px",
    content=[
        html.Div(
            children=[
                mini_card("Project_ID", a_function=dcc.Dropdown(id="new_projectid", 
                    #options=project_options, 
                    style={"width": "130px"})),
                mini_card("Funding", a_function=dcc.Dropdown(id="new_funding", 
                    #options=founding_sources_options, 
                    style={"width": "130px"})),
                mini_card("Topic", a_function=dcc.Input(id="new_topic", type="text", placeholder="", style={"width": "130px"})),
                mini_card("Topic Class", a_function=dcc.Dropdown(id="new_topic_class", 
                    #options=topic_class_options, 
                    style={"width": "130px"})),
                mini_card("Argus enabled", a_function=dcc.Dropdown(id="new_argus", value="Yes", options=[{"label": "Yes", "value": "Yes"}, {"label": "No", "value": "No"}], style={"width": "130px"})),
                small_icon_card(id="projects_add_project", icon="add", color="white"),
                small_icon_card(id="projects_update_project", icon="update", color="white"),
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                mini_card("Way of charging", a_function=dcc.Dropdown(id="new_charging", value="Manual", options=[{"label": "Manual", "value": "Manual"}, {"label": "LRM", "value": "LRM"}], style={"width": "130px"})),
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
                    title="Project Deadlines",
                    size="650px", 
                    height="250px",
                    content=[
                        html.Div(dcc.Loading(id="table_deadlines"))
                    ]
                )
            ]
        ),

        html.Div(
            children=[
                content_card_size(
                    id="sub_card5",
                    title="Costcenters of Team",
                    size="400px", 
                    height="200px",
                    content=[
                        html.Div(dcc.Loading(id="table_team_costcenter"))
                    ]
                ),
                content_card_size(
                    id="sub_card4",
                    title="Project Team",
                    size="650px", 
                    height="200px",
                    content=[
                        html.Div(dcc.Loading(id="table_team"))
                    ]
                ),
                content_card_size(
                    id="sub_card5",
                    title="Project Budget",
                    size="400px", 
                    height="200px",
                    content=[
                        html.Div(dcc.Loading(id="table_yearly_budget"))
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
                mini_card("Team_Member", a_function=dcc.Dropdown(id="single_teammember", style={"width": "130px"})),
                small_icon_card(id="projects_assign_team_add_button", icon="add", color="white"),
                small_icon_card(id="projects_assign_team_delete_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


assigned_costcenter = content_card_size(
    id="assigned_costcenter_content",
    title="Assigned costcenters",
    size="500px", 
    height="200px",
    content=[
        html.Div(dcc.Loading(id="table_assigned_costcenter"))
    ]
)


assign_costcenter = content_card_size(
    id="assign_costcenter",
    title="Assign Costcenter to project",
    size="500px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Costcenter", a_function=dcc.Input(id="costcenter_input", type="text", style={"width": "130px"})),  
                small_icon_card(id="projects_assign_costcenter_add_button", icon="add", color="white"),
                small_icon_card(id="projects_assign_costcenter_delete_button", icon="delete", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


assign_costcenter_project = content_card_size(
    id="assigned_costcenter_project",
    title="Assign Costcenter to Teammember",
    size="700px", 
    height="200px",
    content=[
        html.Div(
            children=[
                #TODO
                mini_card("Costcenter", a_function=dcc.Dropdown(id="costcenter_dropdown", style={"width": "130px"})),
                mini_card("Team_Member", a_function=dcc.Dropdown(id="single_teammember_dropdown", style={"width": "130px"})),
                small_icon_card(id="projects_assignd_costcenter_update_button", icon="update", color="white"),
                small_icon_card(id="projects_assignd_costcenter_delete_button", icon="delete", color="white"),
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
                mini_card("Team_Member", a_function=dcc.Dropdown(id="yearly_single_teammember", style={"width": "130px"})),
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
                            value=this_year
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


gant_card = content_card_size(
    id="gant_card_projects_content",
    title="Project Timeline",
    size="1500px", 
    height="480px",
    content=[
        html.Div(
            [dcc.Loading(id="fig_project_timeline")]
        )
    ]
)


callback_timer = dcc.Interval(id ="update_timer",  interval = 4*1000)  #1000 ms * 4 = 4sec



layout = html.Div(
    children=[
        table_card,
        gant_card,
        aproject_card,
        html.Div(
            children=[
                assigned_team,
                assign_project,
            ],
            style={"display": "flex"}
        ),
        html.Div(
            children=[
                assigned_costcenter,
                assign_costcenter,
                assign_costcenter_project
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

        callback_timer
    ],
    style={"display": "block"}
)





# make the callbacks

# founding sources option list
@dash.callback(
    Output("new_funding", "options"),
    [
        Input("projects_add_project", "n_clicks"),
        Input("update_timer", "n_intervals"),
    ]
)
def update_founding(n_clicks, n_intervals):
    sql= "SELECT founding_source FROM founding_sources"
    data = execute_sql(sql)
    data=pd.DataFrame(data, columns=["founding_source"])
    list_data=list(data["founding_source"])
    list_data.sort()
    founding_sources_options = get_option_list(list_data)

    return founding_sources_options


@dash.callback(
    Output("new_topic_class", "options"),
    [
        Input("projects_add_project", "n_clicks"),
        Input("projects_update_project", "n_clicks")
        # Input("update_timer", "n_intervals"),
    ]
)
def update_founding(n_clicks, update_clicks):

    sql = """
        SELECT topic_class FROM topic_class
    """
    data = execute_sql(sql)
    data=pd.DataFrame(data, columns=["topic_class"])
    list_data=list(data["topic_class"])
    # list_data.sort()
    topic_class_options = get_option_list(list_data)

    return topic_class_options



# teammember option list: single_teammember
@dash.callback(
    Output("single_teammember", "options"),
    [
        Input("new_projectid", "value"),
        Input("projects_add_project", "n_clicks"),
        Input("update_timer", "n_intervals"),
    ]
)
def create_team_members_options(project_id, n_clicks, n_intervals):

    sql = """
        SELECT full_name FROM team_members
    """
    data = execute_sql(sql)
    data=pd.DataFrame(data, columns=["full_name"])
    list_data=list(data["full_name"])
    list_data.sort()
    team_members_options = get_option_list(list_data)

    return team_members_options


# teammember option list: single_teammember_dropdown
@dash.callback(
    [
        Output("yearly_single_teammember", "options"),
        Output("single_teammember_dropdown", "options")
    ],
    [
        Input("new_projectid", "value"),
        Input("projects_assign_team_add_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
    ]
)
def create_team_members_options(project_id, n_clicks, n_intervals):

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

    list_data=list(data["active PrAI Team members"])
    list_data.sort()
    active_team_members_options = get_option_list(list_data)

    return  active_team_members_options, active_team_members_options


# figure callback
@dash.callback(
    Output("fig_project_timeline", "children"),
    [
        Input("projects_year", "value"),
        Input("projects_teammember", "value"),
        Input("projects_assign_team_add_button", "n_clicks"),
        Input("projects_assign_team_delete_button", "n_clicks"),
    ]
)
def create_gant_fig(year, teammember, add_button, delete_button):

    low_year = f"{str(int(year))}"+"-01-01"
    upper_year = f"{str(int(year)+1)}"+"-01-01"

    if teammember != None:

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
                AND
                tm.full_name = '{teammember}'
        """

    else:
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

    data = execute_sql(sql=sql)

    data = pd.DataFrame(data=data, columns = ["project_id", "fullname", "Start", "Finish", "Task", "Topic"])


    if teammember != None:
        data = data[data["fullname"] == teammember]

    data = data.sort_values(by="project_id", ascending=False)
    data = data.reset_index(drop = True)

    # sorted_gant(df=data, Task="project_id", team_member="Task", start_date="Start", end_date="Finish", date=None, plot = True)
    # fig = sorted_gant(df=data, Task="Task", team_member="Task", start_date="Start", end_date="Finish", date=None, plot = False)

    fig = single_gantt(df=data, team_member=teammember, color="Task", Task="Task", Start="Start", Finish="Finish", date=None, plot = False)

    return dcc.Graph(figure=fig)





# project_drop down lists: team & year
@dash.callback(
    [
        Output("projects_year", "options"),
        Output("projects_teammember", "options"),
    ],
    [
        Input("projects_add_project", "n_clicks"),
    ]
    # ,prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_dropdown_options(clicks):

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

    return years_options, team_members_options



@dash.callback(
    Output("new_projectid", "value"),
    [
        Input("projects_table", "selected_rows"),
        Input("projects_table", "data")
    ]
)
def get_projectid_from_projectstable(selected_row, raw_data):

    mdata = pd.DataFrame(data = raw_data)

    scnames=["project_id", "Topic", "Topic_Class", "Founding Source", "Year"]

    selected_data = mdata.loc[selected_row, scnames]
    selected_data = selected_data.reset_index(drop= True)

    project_id = selected_data.loc[0, "project_id"]

    return project_id


# TODO: output project_id, value, select.
# add project
@dash.callback(
    [
    Output("projects_add_project_button", "style"),
    Output("new_projectid", "options"),
    ],
    [
        Input("projects_add_project", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_add_project_button", "style"),
        State("new_funding", "value"),
        State("new_topic", "value"),
        State("new_topic_class", "value"),
        State("new_argus", "value"),
        State("new_charging", "value"),
        State("new_account_responsible", "value"),
        State("new_start", "date"),
        State("new_end", "date"),
        State("new_project_diff", "value"),
        State("new_project_status", "value"),
        State("new_text", "value"),
        State("new_target", "value")
    ]
    # , prevent_initial_call=True
    # , suppress_callback_exceptions=True
)
def projects_add_project(
    n_clicks, 
    n_interval, 
    style,
    funding,
    topic,
    topic_class,
    argus,
    charging,
    account_resp,
    start,
    end,
    difficulty,
    status,
    description,
    target
    ):

    button_id = ctx.triggered_id


    if ((button_id == "projects_add_project") and (style['background-color'] == "white") and (style != None)):

        sql = f"""
            INSERT INTO project (funding_id, topic, topic_class_id, argus_enabled, way_charging, cost_center_respon, start_date, end_date, difficulty, project_status, project_description, project_goals) VALUES 
            (
                (SELECT founding_source_id FROM founding_sources WHERE founding_source = '{funding}'),
                '{topic}',
                (SELECT topic_class_id FROM topic_class WHERE topic_class = '{topic_class}'),
                '{argus}',
                '{charging}',
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

    sql= "SELECT project_id FROM project"
    data=execute_sql(sql)

    data=pd.DataFrame(data, columns=["project_id"])
    list_data=list(data["project_id"])
    list_data.sort(reverse=True)
    project_options = get_option_list(list_data)

    # new_index = list(data["project_id"])[-1]

    return color, project_options


# give values when project id is selected
@dash.callback(
    [
        Output("new_funding", "value"),
        Output("new_topic", "value"),
        Output("new_topic_class", "value"),
        Output("new_argus", "value"),
        Output("new_charging", "value"),
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

        funding = data.loc[0, "funding"]
        topic = data.loc[0, "topic"]
        topic_class = data.loc[0, "topic_class"]
        argus = data.loc[0, "argus"]
        charging = data.loc[0, "charging"]
        account_resp = data.loc[0, "account_resp"]
        start = data.loc[0, "start"]
        end = data.loc[0, "end"]
        difficulty = data.loc[0, "difficulty"]
        status = data.loc[0, "status"]
        description = data.loc[0, "description"]
        target = data.loc[0, "target"]
    
    else:
        funding = topic = topic_class = argus = charging =  account_resp = start = end = difficulty = status = description = target = None

    return funding, topic, topic_class, argus, charging, account_resp, start, end, difficulty, status, description, target


# update_budget_year_limits
@dash.callback(
    [
        Output("budget_year", "min"),
        Output("budget_year", "max"),
        Output("budget_team_year", "min"),
        Output("budget_team_year", "max")
    ],
    [
        Input("new_start", "date"),
        Input("new_end", "date")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_budget_year_limits(start_date, end_date):

    if ((start_date != None) and (end_date != None)):

        year_low = datetime.strptime(start_date, "%Y-%m-%d")
        year_high = datetime.strptime(end_date, "%Y-%m-%d")

        year_low=year_low.year
        year_high =year_high.year

    else:
        year_low = None
        year_high = None

    return year_low, year_high, year_low, year_high


# update project
@dash.callback(
    Output("projects_update_project_button", "style"),
    [
        Input("projects_update_project", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_update_project_button", "style"),
        State("new_projectid", "value"),
        State("new_funding", "value"),
        State("new_topic", "value"),
        State("new_topic_class", "value"),
        State("new_argus", "value"),
        State("new_charging", "value"),
        State("new_account_responsible", "value"),
        State("new_start", "date"),
        State("new_end", "date"),
        State("new_project_diff", "value"),
        State("new_project_status", "value"),
        State("new_text", "value"),
        State("new_target", "value")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_update_project(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    funding,
    topic,
    topic_class,
    argus,
    charging,
    account_resp,
    start,
    end,
    difficulty,
    status,
    description,
    target
    ):

    button_id = ctx.triggered_id



    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_update_project"):

        sql = f"""
            UPDATE project
            SET
            funding_id = (SELECT founding_source_id FROM founding_sources WHERE founding_source = '{funding}'),
            topic = '{topic}',
            topic_class_id = (SELECT topic_class_id FROM topic_class WHERE topic_class = '{topic_class}'),
            argus_enabled = '{argus}',
            way_charging = '{charging}',
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
        State("projects_assign_team_add_button_button", "style"),
        State("new_projectid", "value"),
        State("single_teammember", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_assign_team_add(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    single_teammember
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_assign_team_add_button"):

        if ((project_id != None) and (single_teammember != None)):

            sql = f"""
                INSERT INTO project_team_members(project_id, team_id) VALUES
                (
                    (SELECT project_id FROM project WHERE project_id = '{project_id}'),
                    (SELECT team_id FROM team_members WHERE full_name = '{single_teammember}')
                )
            """
            execute_sql(sql)

            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}
        
        else: 
            color = {"background-color": "white",
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
        State("projects_assign_team_delete_button_button", "style"),
        State("new_projectid", "value"),
        State("single_teammember", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_remove_team(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    teammember
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_assign_team_delete_button"):

        if ((project_id != None) and (teammember != None)):

            sql = f"""
                DELETE FROM project_team_members
                WHERE
                project_id in (SELECT project_id FROM project WHERE project_id = '{project_id}')
                AND
                team_id in (SELECT team_id FROM team_members WHERE full_name = '{teammember}');
            """
            execute_sql(sql)

            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# show up teammember_table
@dash.callback(
    Output("table_assigned_team", "children"),
    [
        Input("projects_update_project", "n_clicks"),
        Input("projects_assign_team_add_button", "n_clicks"),
        Input("projects_assign_team_delete_button", "n_clicks"),
        Input("new_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_teammember_table(update_button, add_button, delete_button, project_id):

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
            id = "table_teammembers",
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



# add project costcenter
@dash.callback(
    Output("projects_assign_costcenter_add_button_button", "style"),
    [
        Input("projects_assign_costcenter_add_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("costcenter_input", "value"),
        State("projects_assign_costcenter_add_button_button", "style"),
        State("new_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_add_costcenter(
    n_clicks, 
    n_interval, 
    costcenter,
    style,
    project_id
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_assign_costcenter_add_button"):

        if costcenter != None:

            sql = f"""
                INSERT INTO project_costcenter(project_id, costcenter) VALUES
                (
                    (SELECT project_id FROM project WHERE project_id = '{project_id}'),
                    '{costcenter}'
                );
            """
            data = execute_sql(sql)
            data
            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}
        else:
            color = {"background-color": "white",
                "height": "70px", 
                "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color



# delete project costcenter
@dash.callback(
    Output("projects_assign_costcenter_delete_button_button", "style"),
    [
        Input("projects_assign_costcenter_delete_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("costcenter_input", "value"),
        State("projects_assign_costcenter_delete_button_button", "style"),
        State("new_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_add_costcenter(
    n_clicks, 
    n_interval, 
    costcenter,
    style,
    project_id
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_assign_costcenter_delete_button"):

        if costcenter != None:

            sql = f"""
                DELETE FROM project_costcenter
                WHERE 
                project_id ='{project_id}'
                AND
                costcenter = '{costcenter}';
            """
            execute_sql(sql)
            data
            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}
        else:
            color = {"background-color": "white",
                "height": "70px", 
                "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# show up costcenter_table
@dash.callback(
    Output("table_assigned_costcenter", "children"),
    [
        Input("projects_assign_costcenter_add_button", "n_clicks"),
        Input("projects_assign_costcenter_delete_button", "n_clicks"),
        Input("new_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_costcenter_table(add_button, delete_button, project_id):

    if (project_id != None):

        sleep(1)

        sql = f"""
            SELECT costcenter FROM project_costcenter
            WHERE 
            project_id ='{project_id}';
        """

        data = execute_sql(sql)

        data = pd.DataFrame(data, columns=["costcenter"])

        df_costcenter = dash_table.DataTable(
            id = "table_costcenter",
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
            row_selectable="single",
        )
    else: 
        df_costcenter = None

    return df_costcenter


# show up costcenter_dropdown for team and project
@dash.callback(
    Output("costcenter_dropdown", "options"),
    [
        Input("projects_assign_costcenter_add_button", "n_clicks"),
        Input("projects_assign_costcenter_delete_button", "n_clicks"),
        Input("new_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_costcenter_dropdown(add_button, delete_button, project_id):

    if (project_id != None):

        sleep(0.5)

        sql = f"""
            SELECT costcenter FROM project_costcenter
            WHERE 
            project_id ='{project_id}';
        """

        data = execute_sql(sql)

        data = pd.DataFrame(data, columns=["costcenter"])

        costcenter_list = list(data["costcenter"])

        return get_option_list(costcenter_list)




# show up asigned team costcenter_table
@dash.callback(
    Output("table_team_costcenter", "children"),
    [
        Input("projects_assignd_costcenter_update_button", "n_clicks"),
        Input("projects_assignd_costcenter_delete_button", "n_clicks"),
        Input("new_projectid", "value"),
    ]
    #, prevent_initial_call=True
    #, suppress_callback_exceptions=True
)
def update_team_costcenter_table(add_button, delete_button, project_id):

    if (project_id != None):

        sleep(1)

        sql = f"""
            SELECT tm.full_name, appc.costcenter 
            FROM active_project_person_costcenter appc
            INNER JOIN team_members tm
            ON appc.team_id = tm.team_id
            WHERE 
            project_id = '{project_id}';
        """
        data = execute_sql(sql)
        data

        data = pd.DataFrame(data=data, columns=["team", "Cost center"])
        data

        if data.shape[0] != 0:
            data = data

        elif data.shape[0] == 0:
            data = pd.DataFrame(data=None, columns=["team", "Cost center"])

        df_costcenter = dash_table.DataTable(
            id = "dashtable_team_costcenter",
            columns=[{"name": str(i), "id": str(i)} for i in data.columns],
            data=data.to_dict("records"),
            style_table={"height": "150px", "overflow": "auto", "width": "300px"},
            style_as_list_view=False,
            style_header={"fontweight": "bold", "font-family": "sans-serif"},
            style_cell={
                "font-family": "sans-serif", 
                'overflow': 'hidden',
                "minWidth": 60
                },
            row_selectable=False,
        )

    else: 
        df_costcenter = None

    return df_costcenter



# small_icon_card(id="projects_assignd_costcenter_update_button", icon="update", color="white"),
# small_icon_card(id="projects_assignd_costcenter_delete_button", icon="delete", color="white"),

# mini_card("Costcenter", a_function=dcc.Dropdown(id="costcenter_dropdown", style={"width": "130px"})),
# mini_card("Team_Member", a_function=dcc.Dropdown(id="single_teammember_dropdown", style={"width": "130px"})),

# update assigned costcentre to team
@dash.callback(
    Output("projects_assignd_costcenter_update_button_button", "style"),
    [
        Input("projects_assignd_costcenter_update_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_assignd_costcenter_update_button_button", "style"),
        State("new_projectid", "value"),
        State("costcenter_dropdown", "value"),
        State("single_teammember_dropdown", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_assign_team_add(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    costcenter,
    teammember
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_assignd_costcenter_update_button"):

        if ((project_id != None) and (teammember != None)):

            # delete

            sql = f"""
                DELETE FROM active_project_person_costcenter
                WHERE
                project_id = '{project_id}'
                AND
                team_id in (SELECT team_id FROM team_members WHERE full_name = '{teammember}');
            """
            data = execute_sql(sql)
            data

            # new insert

            sql = f"""
                INSERT INTO active_project_person_costcenter (project_id, team_id, costcenter) VALUES
                (
                    (SELECT project_id FROM project WHERE project_id = '{project_id}'),
                    (SELECT team_id FROM team_members WHERE full_name = '{teammember}'),
                    '{costcenter}'
                );
            """
            data = execute_sql(sql)

            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}
        
        else: 
            color = {"background-color": "white",
                "height": "70px", 
                "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# delete assigned costcentre to team
@dash.callback(
    Output("projects_assignd_costcenter_delete_button_button", "style"),
    [
        Input("projects_assignd_costcenter_delete_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_assignd_costcenter_delete_button_button", "style"),
        State("new_projectid", "value"),
        State("single_teammember_dropdown", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_assign_team_add(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    teammember
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_assignd_costcenter_delete_button"):

        if ((project_id != None) and (teammember != None)):

            # delete

            sql = f"""
                DELETE FROM active_project_person_costcenter
                WHERE
                project_id = '{project_id}'
                AND
                team_id in (SELECT team_id FROM team_members WHERE full_name = '{teammember}');
            """
            data = execute_sql(sql)
            data

            # new insert

            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}
        
        else: 
            color = {"background-color": "white",
                "height": "70px", 
                "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color




# add project deadline
@dash.callback(
    Output("projects_add_deadline_button_button", "style"),
    [
        Input("projects_add_deadline_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_add_deadline_button_button", "style"),
        State("deadline_date", "date"),
        State("deadline_topic", "value"),
        State("new_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_add_deadline(
    n_clicks, 
    n_interval, 
    style,
    deadline_date,
    deadline_topic,
    project_id
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_add_deadline_button"):

        if ((deadline_date != None) and (deadline_topic != None) and (project_id != None)):

            sql = f"""
                INSERT INTO project_deadlines(project_id, deadline_date, deadline_text) VALUES
                (
                    (SELECT project_id FROM project WHERE project_id = '{project_id}'),
                    '{deadline_date}',
                    '{deadline_topic}'
                );
            """
            data = execute_sql(sql)
            data
            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}
        else:
            color = {"background-color": "white",
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
        State("projects_delete_deadline_button_button", "style"),
        State("deadline_date", "date"),
        State("deadline_topic", "value"),
        State("new_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_remove_deadline(
    n_clicks, 
    n_interval, 
    style,
    deadline_date,
    deadline_topic,
    project_id
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_delete_deadline_button"):

        if ((deadline_date != None) and (deadline_topic != None) and (project_id != None)):

            sql = f"""
                DELETE FROM project_deadlines
                WHERE
                project_id in (SELECT project_id FROM project WHERE project_id = '{project_id}')
                AND
                deadline_date = '{deadline_date}'
                AND
                deadline_text = '{deadline_topic}';
            """
            data = execute_sql(sql)
            data

            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}
        else:
            color = {"background-color": "white",
                "height": "70px", 
                "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# update and create deadline tables
@dash.callback(

    Output("table_deadlines", "children"),
    [
        Input("new_projectid", "value"),
        Input("projects_add_deadline_button", "n_clicks"),
        Input("projects_delete_deadline_button", "n_clicks"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_deadlines_table(project_id, deadline_button, delete_deadline_button):

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
            id = "deadlines_table",
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


# selectable deadline table for updates
@dash.callback(
    [
        Output("deadline_date", "date"),
        Output("deadline_topic", "value")
    ],
    [
        Input("deadlines_table", "selected_rows"),
        Input("deadlines_table", "data"),
        State("new_projectid", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def select_deadline_table(selected_row, raw_data, projectid):

    if ((projectid != None) and (raw_data != None) and (selected_row != None)):

        data = pd.DataFrame(raw_data, columns=["Date", "Topic"])

        date = list(set(data.loc[selected_row, "Date"]))[0]
        topic = list(set(data.loc[selected_row, "Topic"]))[0]
    else:
        date = topic = None

    return date, topic



# project overview table at the end of the page
@dash.callback(

    Output("table_projects_overview", "children"),
    [
        Input("projects_update_project", "n_clicks"),
        Input("projects_add_project", "n_clicks"),
        Input("projects_year", "value"),
        Input("projects_teammember", "value"),
        Input("projects_assign_team_add_button", "n_clicks"),
        Input("projects_assign_team_delete_button", "n_clicks")
    ]
    # , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_table(update_project_button, add_project_button, year, teammember, add_buttton, delete_button):

    if teammember != None:
        sql=f"""
            SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, pbp.year
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
        sql=f"""
            SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, pbp.year
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
        """
    data=execute_sql(sql)

    data = pd.DataFrame(data, columns=["project_id", "Topic", "Topic_Class", "Founding Source", "Year"])

    data = data.sort_values(by="project_id")

    data = data.drop_duplicates(keep="first")

    data = data.reset_index(drop=True)

    df_projects = dash_table.DataTable(
        id = "projects_table",
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




# small_icon_card(id="projects_add_budget_button", icon="add", color="white"),
# add yearly budget to project
@dash.callback(
    Output("projects_add_budget_button_button", "style"),
    [
        Input("projects_add_budget_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_add_budget_button_button", "style"),
        State("new_projectid", "value"),
        State("budget_year", "value"),
        State("yearly_budget", "value")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_add_budget(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    budget_year,
    yearly_budget
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_add_budget_button"):

        if ((project_id != None) and (budget_year != None) and (yearly_budget != None)):

            sql = f"""
                INSERT INTO project_budget_planning (project_id, year, budget) VALUES
                (
                    (SELECT project_id FROM project WHERE project_id = '{project_id}'),
                    '{budget_year}',
                    '{yearly_budget}'
                );
            """

            data=execute_sql(sql)

            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}
        
        else:
            color = {"background-color": "white",
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
        State("projects_update_budget_button_button", "style"),
        State("new_projectid", "value"),
        State("budget_year", "value"),
        State("yearly_budget", "value")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_update_budget(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    budget_year,
    yearly_budget
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_update_budget_button"):

        sql = f"""
            UPDATE project_budget_planning
            SET
            project_id = (SELECT project_id FROM project WHERE project_id = '{project_id}'),
            year = '{budget_year}',
            budget = '{yearly_budget}'
            WHERE project_id = '{project_id}' 
            AND year = '{budget_year}';
        """
        execute_sql(sql)

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
        State("projects_delete_budget_button_button", "style"),
        State("new_projectid", "value"),
        State("budget_year", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_delete_budget(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    budget_year
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_delete_budget_button"):

        if ((project_id != None) and (budget_year != None)):

            sql = f"""
                DELETE FROM project_budget_planning
                WHERE
                project_id in (SELECT project_id FROM project WHERE project_id = '{project_id}')
                AND
                year = '{budget_year}';
                """

            execute_sql(sql)
            color = {"background-color": "green",
                "height": "70px", 
                "width": "70px"}
        
        else:
            color = {"background-color": "white",
                "height": "70px", 
                "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color


# show update project budget table
@dash.callback(

    Output("table_yearly_budget", "children"),
    [
        Input("new_projectid", "value"),
        Input("projects_add_budget_button", "n_clicks"),
        Input("projects_update_budget_button", "n_clicks"),
        Input("projects_delete_budget_button", "n_clicks")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_budget_table(project_id, add_budget, update_budget, delete_budget):

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
            id = "project_budget_table",
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



# small_icon_card(id="projects_add_team_budget_button", icon="add", color="white"),
# budget to some project team members
@dash.callback(
    Output("projects_add_team_budget_button_button", "style"),
    [
        Input("projects_add_team_budget_button", "n_clicks"),
        Input("update_timer", "n_intervals"),
        State("projects_add_team_budget_button_button", "style"),
        State("new_projectid", "value"),
        State("budget_team_year", "value"),
        State("yearly_single_teammember", "value"),
        State("yearly_team_budget", "value")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_add_budget_to_team(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    year,
    teammember,
    teammember_budget
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_add_team_budget_button"):

        sql = f"""
            INSERT INTO team_year_project_budget(project_id, year, team_id, project_yearly_budget) VALUES
            (
                (SELECT project_id FROM project WHERE project_id = '{project_id}'),
                '{year}',
                (SELECT team_id FROM team_members WHERE full_name ='{teammember}'),
                '{teammember_budget}'
            );
        """
        data = execute_sql(sql)

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
        State("projects_update_team_budget_button_button", "style"),
        State("new_projectid", "value"),
        State("budget_team_year", "value"),
        State("yearly_single_teammember", "value"),
        State("yearly_team_budget", "value")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_update_budget_to_team(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    year,
    teammember,
    teammember_budget
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_update_team_budget_button"):


        sql = f"""
            UPDATE team_year_project_budget
            SET
            project_yearly_budget = '{teammember_budget}'
            WHERE project_id = '{project_id}' AND year = '{year}' AND team_id = (SELECT team_id FROM team_members WHERE full_name ='{teammember}');
        """
        execute_sql(sql)

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
        State("projects_delete_team_budget_button_button", "style"),
        State("new_projectid", "value"),
        State("budget_team_year", "value"),
        State("yearly_single_teammember", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def projects_delete_budget_to_team(
    n_clicks, 
    n_interval, 
    style,
    project_id,
    year,
    teammember,
    ):

    button_id = ctx.triggered_id

    if ((button_id == "update_timer") and (style['background-color'] == "green")):
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    elif (button_id == "projects_delete_team_budget_button"):

        sql = f"""
            DELETE FROM team_year_project_budget
            WHERE
            project_id = '{project_id}'
            AND
            year = '{year}'
            AND
            team_id = (SELECT team_id FROM team_members WHERE full_name ='{teammember}');
            """
        execute_sql(sql)

        color = {"background-color": "green",
            "height": "70px", 
            "width": "70px"}

    else: 
        color = {"background-color": "white",
            "height": "70px", 
            "width": "70px"}

    return color



# show update project budget table
@dash.callback(

    Output("table_team", "children"),
    [
        Input("new_projectid", "value"),
        Input("projects_add_team_budget_button", "n_clicks"),
        Input("projects_update_team_budget_button", "n_clicks"),
        Input("projects_delete_team_budget_button", "n_clicks")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_budget_table(project_id, add_budget, update_budget, delete_budget):

    if project_id != None:

        sleep(0.1)

        sql = f"""
            SELECT typb.year, tm.full_name, typb.project_yearly_budget
            FROM team_year_project_budget typb
            INNER JOIN team_members tm
            ON typb.team_id = tm.team_id
            WHERE typb.project_id = '{project_id}'
        """
        data=execute_sql(sql)

        data = pd.DataFrame(data, columns=["Year", "Team member", "Budget"])

        data = data.pivot(index="Team member", columns = "Year", values= "Budget")
        data =data.reset_index(drop=False)

        data = data.sort_values(by="Team member")

        inter_data = pd.DataFrame([["Sum"]+list(data[data.columns].sum(axis=0, numeric_only=True))], columns = data.columns)
        data=pd.concat([data, inter_data], axis=0)

        data["Sum"] = data[data.columns].sum(axis=1, numeric_only=True)

        data = data.reset_index(drop = True)

        df_budget_table = dash_table.DataTable(
            id = "project_team_budget_table",
            columns=[{"name": str(i), "id": str(i)} for i in data.columns],
            data=data.to_dict("records"),
            style_table={"height": "150px", "overflow": "auto", "width": "500px"},
            style_as_list_view=False,
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





