import dash
import datetime

import pandas as pd
from time import sleep
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
    budget_paretoplot
)



dash.register_page(__name__,)

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


booking_timer = dcc.Interval(id ="booking_timer",  interval = 4*1000)  #1000 ms * 4 = 4sec




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
    height="350px",
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
                    # small_icon_card(id="add_button", icon="add", color="white"),
                    small_icon_card(id="update_project_budget_button", icon="update", color="white"),
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
        booking_timer
    ]
)


monthly_working = content_card_size(
    id="monthly_working_content",
    title="Monthly Working Days",
    size="900px", 
    height="350px",
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
                html.Div(id="monthly_working_div")
            ]
        )
    ]
)

monthly_budget = content_card_size(
    id="monthly_budget_content",
    title="Monthly budget Bookings",
    size="1100px", 
    height="350px",
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
                html.Div(id="monthly_budget_div")
            ]
        )
    ]
)


entity_budget = content_card_size(
    id="monthly_budget_content",
    title="Required Budget",
    size="300px", 
    height="350px",
    content=[
        mini_card("Full Coverage", a_function=dcc.Loading(id="coverage_budget", style={"width": "130px"})),
        ]
    )


paretro_graph = content_card_size(
    id = "paretro_graph_content",
    title = "Paretro Plot of Budget",
    size = "1500px",
    height="500px",
    content=[
        dcc.Loading(id="load_paretro_graphic")
    ]
)


layout = html.Div(
    children=[
        html.Div(children=[
            table_card,
            entity_budget
        ],
        style={"display": "flex"}),
        html.Div(children=[
            monthly_working,
            monthly_budget
        ],
        style={"display": "flex"}),
        paretro_graph
    ],
    style={"display": "block"}
)



@dash.callback(
    Output("coverage_budget", "children"),
    [
        Input("overview_year", "value"),
        Input("overview_teammember", "value"),
    ]
    # ,prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def show_eff_coverage(overview_year, overview_teammember):

    sql = f"""
        SELECT tm.full_name, ti.year, ti.contract, ti.working_month, ti.activity, et.coverage
        FROM team_members tm
        INNER JOIN team_info ti
        ON tm.team_id = ti.team_id
        INNER JOIN entity_time et
        ON et.entity_id = tm.legal_entity_id and ti.year = et.year
        WHERE tm.full_name = '{overview_teammember}'
        AND
        ti.year = '{overview_year}'
    """
    data = execute_sql(sql)

    df = pd.DataFrame(data, columns=["Fullname", "Year", "Contract", "Working Month", "Activity", "Coverage"])

    df["eff. Coverage"] = round(df["Contract"] * df["Working Month"] * df["Coverage"] * 1/100 * 1/12, 1)

    result=df["eff. Coverage"][0]


    return html.H3(result)





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
        # row_selectable="single",
        row_selectable=False,
    )

    return df_projects



@dash.callback(

    Output("monthly_working_div", "children"),
    [
        Input("overview_year", "value"),
        Input("overview_teammember", "value"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_work_table(
    overview_year, 
    overview_teammember):

    sleep(0.3)


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
    data = pd.DataFrame(data, columns=["project_id", "topic", "topic_class", "founding_source", "project_descrition"])


    list_ids = list(set(data["project_id"]))


    sql = f"""
        SELECT project_id, month, working_days FROM project_time_budget
        WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
        AND year = '{overview_year}';
    """

    data=execute_sql(sql = sql)

    data = pd.DataFrame(data, columns=["project_id", "month", "working_days"])

    try:
        list_ids_available = list(set(data["project_id"]))
    except BaseException:
        list_ids_available = []


    ids = [element for element in list_ids if element not in list_ids_available]

    data=data.pivot(index="project_id", columns="month", values="working_days")
    data = data.reset_index(drop = False)
    data = data.reset_index(drop = True)
    pda = data

    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    all_zero = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    data = pd.DataFrame()

    if len(data) == 0:
        for id in ids:
            new_data = pd.DataFrame()
            new_data["month"] = months
            new_data["working_days"] = all_zero
            new_data["project_id"] = id
            data = pd.concat([data, new_data], axis=0)

    if len(data) != 0:
        data=data.pivot(index="project_id", columns="month", values="working_days")
        data = data.reset_index(drop = False)
        data = data.reset_index(drop = True)
        pdata = data
        pdata
    else:
        pdata = None

    new_df = pd.concat([pda, pdata], axis=0)
    new_df = new_df.reset_index(drop = True)


    data = new_df


    data = data.sort_values(by="project_id")

    df_budget_table = dash_table.DataTable(
        id = "project_monthly_work_table",
        columns=[{"name": str(i), "id": str(i)} for i in data.columns],
        data=data.to_dict("records"),
        style_table={"height": "300px", "overflow": "auto", "width": "850px"},
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


@dash.callback(

    Output("monthly_budget_div", "children"),
    [
        Input("overview_year", "value"),
        Input("overview_teammember", "value"),
        Input("update_project_budget_button", "n_clicks"),
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_budget_table(
    overview_year, 
    overview_teammember,
    update_clicks
    ):

    sleep(0.9)

    sql = f"""
        SELECT project_id, month, working_days, working_booking FROM project_time_budget
        WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
        AND year = '{overview_year}';
    """

    data=execute_sql(sql = sql)
    data = pd.DataFrame(data, columns=["project_id", "month", "working_days", "working_booking"])
    data = data.pivot(index="project_id", columns="month", values="working_booking")
    data = data.reset_index(drop = False)
    data = data.reset_index(drop = True)

    data = data.sort_values(by="project_id")


    list_sum = ["sum"]+list(round(data[data.columns[1:]].sum(axis=0, numeric_only=True), 2))
    inter_data = pd.DataFrame([list_sum], columns = data.columns)
    data=pd.concat([data, inter_data], axis=0)

    data["Sum"] = round(data[data.columns[1:]].sum(axis=1, numeric_only=True),2)

    data = data.reset_index(drop = True)


    # merge with assigned budget
    sql = f"""
        SELECT typb.project_id, typb.project_yearly_budget
        FROM team_year_project_budget typb
        INNER JOIN team_members tm
        ON typb.team_id = tm.team_id
        WHERE typb.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
        AND
        typb.year = '{overview_year}'
    """
    fdata=execute_sql(sql)

    fdata = pd.DataFrame(fdata, columns=["project_id", "assigned budget"])

    mdata=pd.merge(left=data, right=fdata, left_on="project_id", right_on="project_id")


    list_sum = ["sum"]+list(round(mdata[mdata.columns[1:]].sum(axis=0, numeric_only=True), 2))
    inter_mdata = pd.DataFrame([list_sum], columns = mdata.columns)
    mdata=pd.concat([mdata, inter_mdata], axis=0)

    initial_row = mdata.shape[0]-1


    # make table
    df_budget_table = dash_table.DataTable(
        id = "project_monthly_budget_table",
        columns=[{"name": str(i), "id": str(i)} for i in mdata.columns],
        data=mdata.to_dict("records"),
        style_table={"height": "300px", "overflow": "auto", "width": "1000px"},
        style_as_list_view=False,  #True
        editable=False,
        style_header={"fontweight": "bold", "font-family": "sans-serif"},
        fixed_rows={'headers': True},
        style_cell={
            "font-family": "sans-serif", 
            'overflow': 'hidden',
            "minWidth": 80,
            },
        row_selectable="single",
        selected_rows=[initial_row]
    )

    return df_budget_table



@dash.callback(

    Output("update_project_budget_button", "style"),
    [
        Input("update_project_budget_button", "n_clicks"),
        Input("booking_timer", "n_intervals"),
        State("update_project_budget_button_button", "style"),
        State("overview_year", "value"),
        State("overview_teammember", "value"),
        State("project_monthly_work_table", "data")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def update_project_budget_table( 
    update_button, 
    intervals,
    style,
    overview_year, 
    overview_teammember,
    data):

    button_id = ctx.triggered_id

    if (button_id == "update_project_budget_button"):

        # load raw data from interactive data table
        rawdata =pd.DataFrame(data, columns=["project_id", "1","2","3","4","5","6","7","8","9","10","11","12"])

        sql = f"""
            DELETE from project_time_budget
            WHERE
            team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
            AND
            year = '{overview_year}';
        """
        odata=execute_sql(sql = sql)
        odata


        months = [1,2,3,4,5,6,7,8,9,10,11,12]

        for project_id in list(rawdata["project_id"]):

            selected_data = rawdata.loc[rawdata["project_id"]==project_id]
            selected_data = selected_data.reset_index(drop = True)
            working_days = list(selected_data.loc[0, ["1","2","3","4","5","6","7","8","9","10","11","12"]])

            for i in list(range(len(months))):

                sql = f"""
                    INSERT INTO project_time_budget (year, month, working_days, team_id, project_id) VALUES
                    (
                        '{overview_year}',
                        '{months[i]}',
                        '{working_days[i]}',
                        (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}'),
                        '{project_id}'
                    );
                """
                output=execute_sql(sql = sql)
                output


        # caclulate booking from working days
        sql = f"""
            SELECT ptb.project_id, ptb.team_id, ptb.year, ptb.month, ptb.working_days, ROUND(ptb.working_days*et.coverage/240::numeric,2)
            FROM project_time_budget ptb
            INNER JOIN team_members tm
            ON tm.team_id = ptb.team_id
            INNER JOIN entity_time et
            ON et.entity_id = tm.legal_entity_id
            WHERE ptb.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
            AND ((ptb.year = '{overview_year}') AND (et.year = '{overview_year}'));
        """
        data=execute_sql(sql = sql)

        data = pd.DataFrame(data, columns=["project_id", "team_id", "year", "month", "working_days", "working_bookings"])
        data = data.pivot(index="project_id", columns="month", values="working_bookings")


        # for loop to update
        for project_id in list(data.index):
            for month in list(data.columns):
                money = data.loc[project_id, month]
                sql = f"""
                    UPDATE project_time_budget
                    SET 
                    working_booking = '{money}'
                    WHERE 
                    project_id = '{project_id}' 
                    AND year = '{overview_year}'
                    AND month = '{month}'
                    AND team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}');
                """
                execute_sql(sql)

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



@dash.callback(
    Output("load_paretro_graphic", "children"),
    [
        Input("project_monthly_budget_table", "selected_rows"),
        Input("project_monthly_budget_table", "data")
    ]
    , prevent_initial_call=True
    , suppress_callback_exceptions=True
)
def create_paretro_budget(selected_row, raw_data):

    if selected_row != None:

        cnames = ["project_id",  "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "Sum", "assigned budget"]

        mdata = pd.DataFrame(data = raw_data)
        mdata = mdata.loc[:, cnames]

        scnames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

        selected_data = mdata.loc[selected_row, scnames]
        selected_data = selected_data.reset_index(drop= True)
        selected_data = list(selected_data.iloc[0,:])

        fig = budget_paretoplot(list_of_names=scnames, 
            list_of_values = selected_data, 
            sum_value=mdata.loc[selected_row, "assigned budget"].reset_index(drop=True)[0], 
            yname="k€ booked Budget", 
            xname="Month", 
            title="Budget plan", 
            plot=False)

        return dcc.Graph(figure=fig)
    
    else:
        return html.H3("choose a row")
