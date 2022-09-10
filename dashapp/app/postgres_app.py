import dash
from dash import Dash, html, dcc

from app.utilities.sidebar_utils import (
    icon_and_text
)
# from dashapp.app.utilities.sidebar_utils import (
#     icon_and_text
# )


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
        # html.Div(
        #     dcc.Link('1st', href=dash.page_registry['pages.home']['path'])
        #     ),
        # html.Div(
        #     dcc.Link('2nd', href=dash.page_registry['pages.secondpage']['path'])
        #     ),
        icon_and_text(id="side_user", text="Team", icon="people", href=dash.page_registry['pages.team']['path']),
        icon_and_text(id="side_project", text="Projects", icon="solution", href=dash.page_registry['pages.projects']['path']),
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




# if __name__ == "__main__":
#     app.run_server(port=8050, debug=True)
