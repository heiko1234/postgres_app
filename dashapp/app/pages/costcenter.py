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


costcenter_card=content_card_size(
    id="costcenter_table", 
    title="Calculate Yearly Coverage",
    content=[html.Div(
        children=
            [
                html.H3("Data Table"),
                html.Div(
                    [
                        dash_table.DataTable(
                            id="computed-table",
                            columns=[
                                {"name": "1", "id": "1"},
                                {"name": "2", "id": "2"},
                                {"name": "3", "id": "3"},
                                {"name": "4", "id": "4"},
                                {"name": "5", "id": "5"},
                                {"name": "6", "id": "6"},
                                {"name": "7", "id": "7"},
                                {"name": "8", "id": "8"},
                                {"name": "9", "id": "9"},
                                {"name": "10", "id": "10"},
                                {"name": "11", "id": "11"},
                                {"name": "12", "id": "12"},
                                {"name": "Sum", "id": "sum"},
                            ],
                            data=[
                                {
                                    "1": 0,
                                    "2": 0,
                                    "3": 0,
                                    "4": 0,
                                    "5": 0,
                                    "6": 0,
                                    "7": 0,
                                    "8": 0,
                                    "9": 0,
                                    "10": 0,
                                    "11": 0,
                                    "12": 0
                                },
                            ],
                            editable=True,
                            style_table={"height": "150px", "overflow": "auto", "width": "1250px"},
                            style_as_list_view=True,
                            style_header={"fontweight": "bold", "font-family": "sans-serif"},
                            style_cell={
                                "font-family": "sans-serif", 
                                'overflow': 'hidden',
                                "minWidth": 60
                                },
                        )
                    ]
                )
            ],
        ),
    ],
    size="1300px",
    height="200px"
)


layout = html.Div(
    children=[
        costcenter_card
    ],
    style={"display": "block"}
)






# callbacks


@dash.callback(
    Output('computed-table', 'data'),
    Input('computed-table', 'data_timestamp'),
    State('computed-table', 'data'))
def update_columns(timestamp, rows):
    for row in rows:
        try:
            row['sum'] = round((float(row['1']) + float(row['2']) +float(row['3'])+float(row['4'])+float(row['5'])+float(row['6'])+float(row['7'])+float(row['8'])+float(row['9'])+float(row['10'])+float(row['11'])+float(row['12']))/12, 2)
        except:
            row['sum'] = "NA"
    return rows






