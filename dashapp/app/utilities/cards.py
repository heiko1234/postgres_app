from dash import html, dcc
import base64



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
    img_path = str(f"./dashapp/app/assets/{icon}.png")
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
