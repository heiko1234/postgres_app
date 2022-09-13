import dash

import pandas as pd
from time import sleep
import datetime
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


add_entity_card = content_card_size(
    id="add_entity_content",
    title="Add an Entity",
    size="400px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Legal Entity", a_function=dcc.Input(id="add_entity", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_entity_button", icon="add", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


update_coverage_entity = content_card_size(
    id="add_entity_content",
    title="Update Entity Coverage",
    size="800px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Legal Entity", a_function=dcc.Dropdown(id="dd_entity", style={"width": "130px"})),
                mini_card("Year", a_function=dcc.Input(id="dd_year", type="number", min=2000, max=2100, step=1, value=this_year, style={"width": "130px"})),
                mini_card("Coverage", a_function=dcc.Input(id="coverage_entity", type="number", min=0, max=1000, value=200, style={"width": "130px"})),
                small_icon_card(id="update_entity", icon="update", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)


table_card = content_card_size(
    id="table_card_content",
    title="Yearly Coverage of Entities",
    size="1224px", 
    height="250px",
    content=[
        html.Div(
            children=[
                html.Div(
                    [
                        dcc.Loading(id="table_card_id")
                    ]
                )
            ],
            style={"display": "block"}
        ),
    ]
)




add_founding_card = content_card_size(
    id="add_founding_content",
    title="Add an Founding Source",
    size="400px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Founding Source", a_function=dcc.Input(id="add_founding_source", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_source_button", icon="add", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)

add_topic_class_card = content_card_size(
    id="add_topic_class_content",
    title="Add an Topic Class",
    size="400px", 
    height="200px",
    content=[
        html.Div(
            children=[
                mini_card("Topic Class", a_function=dcc.Input(id="add_topic_class", type="text", placeholder="", style={"width": "130px"})),
                small_icon_card(id="add_topic_button", icon="add", color="white"),
            ],
            style={"display": "flex"}
        ),
    ]
)





layout = html.Div(
    children=[
        html.Div(
            children=[
                add_entity_card,
                update_coverage_entity
            ],
            style={"display": "flex"}
        ),
        table_card,
        html.Div(
            children=[
                add_founding_card,
                add_topic_class_card
            ],
            style={"display": "flex"}
        )
    ],
    style={"display": "block"}
)



@dash.callback(
    Output("add_entity_button", "style"),
    # Output("a_session_store", "data"),
    [
        Input("add_entity_button_button", "n_clicks"),
        State("add_entity", "value"),
    ]
    ,prevent_initial_call=True
)
def new_entity(n_clicks, new_entity):

    color = {"background-color": "white"}

    result = None

    if new_entity != None:

        sql = f"""
            INSERT INTO entity(entity_name) VALUES('{new_entity}')
        """

        try: 
            result = execute_sql(sql)
        except BaseException:
            result = None

        if result == "Done":
            color = {"background-color": "green"}

        else:
            color = {"background-color": "red"}
    
    else:
        color = {"background-color": "white"}

    return color


@dash.callback(
    [   
        Output("dd_entity", "options"),
        Output("dd_entity", "value"),
        # Output("update_entity_color", "style"),
    ],
    [
        Input("update_entity_button", "n_clicks"),
    ]
)
def entity_dropdown(n_clicks):

    sql = """
        SELECT entity_name FROM entity
    """
    data = execute_sql(sql)
    data

    data=pd.DataFrame(data, columns=["OD"])
    list_data=list(data["OD"])
    list_data.sort()
    # list_data

    dict_list = get_option_list(list_data)

    first_choise = list_data[0]

    # color = {"background-color": "green"}

    return dict_list, first_choise




@dash.callback(
    Output("update_entity", "style"),
    [
        Input("update_entity_button", "n_clicks"),
        State("dd_year", "value"),
        State("dd_entity", "value"),
        State("coverage_entity", "value")
    ]
    ,prevent_initial_call=True
)
def new_entity(n_clicks, dd_year, dd_entity, coverage_entity):

    color = {"background-color": "white"}


    sql = f"""
            DELETE from entity_time 
            WHERE
            entity_id in (SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}')
            AND
            entity_time.year = '{dd_year}';
    """
    data=execute_sql(sql = sql)
    data


    sql = f"""
        INSERT INTO entity_time (year, entity_id, coverage) VALUES 
        ('{dd_year}', (SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}'),('{coverage_entity}'));
    """
    data=execute_sql(sql = sql)
    data

    return color


@dash.callback(
    Output("table_card_id", "children"),
    [
        Input("update_entity", "n_clicks"),
    ]
    # ,prevent_initial_call=True
)
def call_data(n_clicks):

    sleep(0.5)

    sql = """
        SELECT et.year, e.entity_name, et.coverage
        FROM entity_time et
        INNER JOIN entity e
        ON e.entity_id = et.entity_id;
    """

    data=execute_sql(sql = sql)

    data = pd.DataFrame(data, columns=["Year", "Entity", "Coverage"])

    pdata=data.pivot(index="Entity", columns="Year", values="Coverage")
    pdata = pdata.reset_index(drop=False)
    pdata = pdata.reset_index(drop = True)
    # pdata


    output_df = dash_table.DataTable(
        id = "table_entity_time",
        columns=[{"name": str(i), "id": str(i)} for i in pdata.columns],
        data=pdata.to_dict("records"),
        style_table={"height": "200px", "overflow": "auto", "width": "1200px"},
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
    Output("add_source_button", "style"),
    [
        Input("add_source_button_button", "n_clicks"),
        State("add_founding_source", "value"),
    ]
    ,prevent_initial_call=True
)
def new_founding(n_clicks, new_source):

    color = {"background-color": "white"}

    result = None

    if new_source != None:

        sql = f"""
            INSERT INTO founding_sources(founding_source) VALUES('{new_source}')
        """

        result = execute_sql(sql)

        if result == "Done":
            color = {"background-color": "green"}

        else:
            color = {"background-color": "red"}
    
    else:
        color = {"background-color": "white"}

    return color


# mini_card("Topic Class", a_function=dcc.Input(id="add_topic_class", type="text", placeholder="", style={"width": "130px"})),
# small_icon_card(id="add_topic_button", icon="add", color="white"),

@dash.callback(
    Output("add_topic_button", "style"),
    [
        Input("add_topic_button_button", "n_clicks"),
        State("add_topic_class", "value"),
    ]
    ,prevent_initial_call=True
)
def new_topic(n_clicks, new_topic):

    color = {"background-color": "white"}

    result = None

    if new_topic != None:

        sql = f"""
            INSERT INTO topic_class(topic_class) VALUES('{new_topic}')
        """

        result = execute_sql(sql)

        if result == "Done":
            color = {"background-color": "green"}

        else:
            color = {"background-color": "red"}
    
    else:
        color = {"background-color": "white"}

    return color




