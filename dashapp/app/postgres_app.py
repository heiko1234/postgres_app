import dash
from dash import Dash, html, dcc

from app.utilities.sidebar_utils import (
    icon_and_text
)


from flask import Flask

server = Flask(__name__)

# session store
a_session_store = dcc.Store(
    id = "a_session_store", storage_type="session"
)

# localhost/dashapp/pages_id
url_base_pathname="/dashapp"

app = Dash(
    __name__, 
    server = server,
    url_base_pathname="/dashapp/",
    use_pages=True
    )

app.title = "Project Database"

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
        icon_and_text(id="side_user", text="Team", icon="user", href=url_base_pathname+dash.page_registry['pages.team']['path']),
        icon_and_text(id="side_project", text="Projects", icon="idea", href=url_base_pathname+dash.page_registry['pages.projects']['path']),
        icon_and_text(id="side_planning", text="Planning", icon="project_planning", href=url_base_pathname+dash.page_registry["pages.planning"]["path"]),
        icon_and_text(id="side_booking", text="Booking", icon="money1", href=url_base_pathname+dash.page_registry['pages.booking']['path']),
        icon_and_text(id="side_analysis", text="Analysis", icon="account", href=url_base_pathname+dash.page_registry['pages.analysis']['path']),
        dcc.Markdown("\n---\n"),
        icon_and_text(id="side_search", text="Search", icon="search", href=url_base_pathname+dash.page_registry["pages.search"]["path"]),
        dcc.Markdown("\n---\n"),
        icon_and_text(id="side_controlling", text="Controlling", icon="analysis6", href=url_base_pathname+dash.page_registry["pages.project_controlling"]["path"]),
        dcc.Markdown("\n---\n"),
        icon_and_text(id="side_construct", text="Construct", icon="construct3", href=url_base_pathname+dash.page_registry['pages.construct']['path']),
        icon_and_text(id="side_costcenter", text="Costs", icon="account2", href=url_base_pathname+dash.page_registry["pages.costcenter"]["path"]),
        dcc.Markdown("\n---\n"),
        # icon_and_text(id="side_increase", text="Benefit", icon="increase", href=url_base_pathname+dash.page_registry['pages.increase']['path']),
    ],
    className="sidebar"
)

app.layout = html.Div(
    [
        sidebar,
        a_session_store,
        html.Div(
            [
                dash.page_container
            ],
            className="content",
        ),
    ]
)



