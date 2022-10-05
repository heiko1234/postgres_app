

from pydoc import classname
from dash import html, dcc
import base64


def hexagon_card(
    id,
    icon,
    text,
):
    if icon != None:
        img_path = str(f"./dashapp/app/assets/{icon}.png")
        encoded_img = base64.b64encode(open(img_path, "rb").read())

    output = html.Div(
        className="hexa", 
        id = id,
        children=[
            html.Div(
                className="hexa_content",
                children=[
                    # html.H1(text),
                    html.Img(
                        id=id+str("_img"), src='data:image/png;base64,{}'.format(encoded_img.decode()),
                        style={
                            "height": "150px", 
                            "width": "150px", 
                            }
                    ),
                ]
            )
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