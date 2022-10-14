

# https://codepen.io/adamriguez/embed/eRaXeq?height=316&theme-id=0&default-tab=result

from pydoc import classname
from dash import html, dcc
import base64


def hexagon_card(
    id,
    icon,
    text,
    href
):
    # if icon != None:
    #     img_path = str(f"./dashapp/app/assets/{icon}.png")
    #     encoded_img = base64.b64encode(open(img_path, "rb").read())

    output = html.Div(
        className="hexa", 
        id = id,
        children=[
            html.Div(
                className="hexa_content",
                children=[
                    dcc.Link(children=[
                        html.H1(text, id = "hexa_content_h1")
                        ],
                        style={"color": "white"},
                        href=href)
                    ]
                )
            ],
            style={
                "background-image": f"url('./assets/{icon}.png')",
                "background-position": "center",
                "background-repeat": "no-repeat",
                "background-size": "150px",
                }
    )

    return output