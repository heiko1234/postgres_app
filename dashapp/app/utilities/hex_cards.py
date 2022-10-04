

from pydoc import classname
from dash import html, dcc
import base64


def hexagon_card(
    id,
    #icon,
    text,
    subtext
):
    # if icon != None:
    #     img_path = str(f"./dashapp/app/assets/{icon}.png")
    #     encoded_img = base64.b64encode(open(img_path, "rb").read())

    output = html.Div(
        className="hexa", 
        id = id,
        children=[
            html.H1(text),
            html.P(subtext)
        ]
    )


    # output = html.Li(
    #             className="hex",
    #             children=[
    #                 # html.A(
    #                 #     className="hexLink"
    #                 # ),
    #                 html.Div(
    #                     className="img",
    #                     style={"background-image": encoded_img}
    #                 ),
    #                 html.Div(
    #                     className="hexIn",
    #                     children=[
    #                         html.A(
    #                             className="hexLink",
    #                             children=[
    #                                 html.H1(text),
    #                                 html.H1(""),
    #                                 html.P(subtext)
    #                             ]
    #                         )
    #                     ]
    #                 )
    #     ]
    # )

    return output