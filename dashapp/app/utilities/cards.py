from dash import html, dcc
import base64
import os


from dotenv import load_dotenv

load_dotenv()

local_run = os.getenv("LOCAL_RUN")
local_run



def content_card(
    id,
    title,
    content
):
    header = html.Div(
        className="content_header",
        children=[
            html.Div(
                title,
            )
        ],
        style={"display": "flex"}
    )
    card = html.Div(
        id=id,
        className="content_card",
        children=[header, html.H3(""), *content],
    )

    return card


def content_card_size(
    id,
    title,
    content,
    size="200px",
    height="300px"

):
    header = html.Div(
        className="content_header",
        children=[
            html.Div(
                title,
            )
        ],
        style={"display": "flex"}
    )
    card = html.Div(
        id=id,
        className="content_card_size",
        children=[header, html.H3(""), *content],
        style={"width": size, "height": height}
    )

    return card


def main_hex_card_size(
    id,
    content
):
    card = html.Div(
        id=id,
        className="main_hex_card",
        children=[html.H3(""), *content],
    )
    return card


def mini_card(text, a_function):
    output = html.Div(
        className="mini_card_class",
        children=[
            html.Span(text),
            html.H3(""),
            a_function
        ],
    )
    return output


def medium_card(id, text, a_function):
    output = html.Div(
        id = id,
        className="medium_card_class",
        children=[
            html.Span(text),
            html.H3(""),
            a_function
        ],
    )
    return output



# not final, icon centered but not on right side
def icon_card(
    id,
    title,
    text,
    icon,
    color="white"
):
    if local_run:
        img_path = str(f"./dashapp/app/assets/{icon}.png")
    else:
        img_path = str(f"./app/assets/{icon}.png")
    encoded_img = base64.b64encode(open(img_path, "rb").read())

    output = html.Div(
        id = id,
        className="icon_card",
        children=[
            html.Div(
                className="icon_card_text",
                children=[
                    html.H3(title, style={"text-align": "left"}),
                    html.H5(text, style={"text-align": "left", "padding": "0rem",}),
                ],
                style={
                        "padding": "0rem", 
                }
            ),
            html.Div(
                className="icon_card_img",
                children=[
                    html.Img(src='data:image/png;base64,{}'.format(encoded_img.decode()),
                    style={
                        "height": "90px", 
                        "width": "90px", 
                        # "align-item":"bottom"
                        })
                ],
                style={"background-color": color,
                    "height": "95px", 
                    "width": "95px",
                    # "align-item":"bottom",
                    }
            )
        ],
        style={"display": "flex"}
    )

    return output


def small_icon_card(
    id,
    icon,
    color="white"
):
    if local_run:
        img_path = str(f"./dashapp/app/assets/{icon}.png")
    else:
        img_path = str(f"./app/assets/{icon}.png")
    encoded_img = base64.b64encode(open(img_path, "rb").read())

    output = html.Div(
        id = id,
        className="small_icon_card",
        children=[
            html.Div(
                id=id+str("_color"),
                className="icon_card_img",
                children=[
                    html.Img(id=id+str("_button"), src='data:image/png;base64,{}'.format(encoded_img.decode()),
                    style={
                        "height": "70px", 
                        "width": "70px", 
                        "background-color": "white"
                        })
                ],
                style={"background-color": color,
                    "height": "70px", 
                    "width": "70px",
                    }
            )
        ],
    )

    return output



def icon_action_card(
    id,
    button_text,
    button_id,
    icon,
    color="white"
):
    if local_run:
        img_path = str(f"./dashapp/app/assets/{icon}.png")
    else:
        img_path = str(f"./app/assets/{icon}.png")
    encoded_img = base64.b64encode(open(img_path, "rb").read())

    output = html.Div(
        id = id,
        className="icon_card",
        children=[
            html.Div(
                html.Button(button_text, id=button_id, n_clicks=0, style={"width": "130px", "height": "50px",'font-size': '20px', "align-item": "center"}),
                style={
                    "height": "90px", 
                    "width": "240px",
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                }
            ),
            html.Div(
                className="icon_card_img",
                children=[
                    html.Img(src='data:image/png;base64,{}'.format(encoded_img.decode()),
                    style={
                        "height": "90px", 
                        "width": "90px", 
                        # "align-item":"bottom"
                        })
                ],
                style={"background-color": color,
                    "height": "95px", 
                    "width": "95px",
                    # "align-item":"bottom",
                    }
            )
        ],
        style={"display": "flex", "align-item": "center"}
    )

    return output


