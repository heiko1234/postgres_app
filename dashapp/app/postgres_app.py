import dash
from dash import Dash, html, dcc

from app.utilities.sidebar_utils import (
    icon_and_text
)


# session store
a_session_store = dcc.Store(
    id = "a_session_store", storage_type="session"
)


app = Dash(__name__, use_pages=True)



sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("Project DB", style={"color": "white"}),
            ],
            className="sidebar-header",
            ),
        html.Div(
            dcc.Markdown("\n---\n")
        ),
        icon_and_text(id="side_user", text="Team", icon="user", href=dash.page_registry['pages.team']['path']),
        icon_and_text(id="side_project", text="Projects", icon="idea", href=dash.page_registry['pages.projects']['path']),
        icon_and_text(id="side_increase", text="Benefit", icon="increase", href=dash.page_registry['pages.projects']['path']),
    ],
    className="sidebar"
)


app.layout = html.Div(
    [
        sidebar,
        html.Div(
            [
                dash.page_container
            ],
            className="content",
        ),
    ]
)



