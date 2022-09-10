import dash
from dash import html, dcc


dash.register_page(__name__, path='/')


# dash.register_page(
#     __name__,
#     path='/home',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


layout = html.Div(children=[
    html.H1(children='This is our Home page'),

    html.Div(children='''
        This is our Home page content.
    '''),
], style={"color":"black"}
)
