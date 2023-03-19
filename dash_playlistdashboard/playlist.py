from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
# Define the layout of the Dash app

def create_accordion_label(song_name, image, preview_url):
    return dmc.AccordionControl(
        dmc.Group(dbc.Row(
            [
                dbc.Col(dmc.Avatar(src=image, radius="xl", size="lg"), width=3),
                dbc.Col(
                    [
                        dmc.Text(song_name),
                        html.Audio(src=preview_url, controls=True, className="mw-100"),
                    ], width=9
                ),
            ]
        )
        ))

def gen_card(track):
    card = dbc.Card([
        dbc.CardImg(
            src=track.album_img
        ),
        dbc.CardImgOverlay(
            [
                dbc.CardHeader(
                    "Music Infos", style={"color": "white", "textAlign": "right"}
                ),
                dbc.CardBody(
                    [
                        html.H5(
                            track.name,
                            className="card-title",
                            style={"textAlign": "right", "fontWeight": "bold"},
                        ),
                        html.P(
                            "This is some card content that we'll reuse",
                            className="card-text",
                            style={"textAlign": "right"},
                        ),
                    ]
                ),
            ]
        ),
    ], id=track.id, style={"top": "1rem", "fontColor": "white"})
    return card


def render_dashplaylistlayout(track_lst, playlist_name):
    #print([i for i in track_lst])
    layout = html.Div(
    [
        dbc.Row(
            dbc.NavbarSimple(
                fixed=True,
                brand="Spotify",
                brand_style={
                    "fontSize": "24px",
                    "fontWeight": "bold",
                    "LineHeight": "1",
                },
                dark=True,
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="#")),
                    dbc.NavItem(dbc.NavLink("About", href="#")),
                    dbc.NavItem(dbc.NavLink("Contact", href="#")),
                ],
            ),
        ),
        dbc.Row(
            [
                dbc.Col(
                    dmc.Aside(
                        p="md",
                        left=0,
                        style={"overflowY": "scroll"},
                        children=[
                            html.H4(playlist_name),
                            dmc.Accordion(
                                chevronPosition="right",
                                variant="contained",
                                id = "playlist-accordion",
                                value = None,
                                children=[
                                    dmc.AccordionItem(
                                        [
                                            create_accordion_label(
                                                track.name,
                                            track.album_img,
                                            track.preview_url,
                                            ),
                                        ],
                                        value=track.id,
                                    )
                                    for track in track_lst
                                ],
                                styles={
                                    "root": {
                                        "backgroundColor": dmc.theme.DEFAULT_COLORS[
                                            "gray"
                                        ][0],
                                        "borderRadius": 5,
                                    },
                                    "item": {
                                        "backgroundColor": dmc.theme.DEFAULT_COLORS[
                                            "gray"
                                        ][0],
                                        "border": "1px solid transparent",
                                        "position": "relative",
                                        "zIndex": 0,
                                        "transition": "transform 150ms ease",
                                        "&[data-active]": {
                                            "transform": "scale(1.03)",
                                            "backgroundColor": "white",
                                            "boxShadow": 5,
                                            "borderColor": dmc.theme.DEFAULT_COLORS[
                                                "gray"
                                            ][2],
                                            "borderRadius": 5,
                                            "zIndex": 1,
                                        },
                                    },
                                    "chevron": {
                                        "&[data-rotate]": {
                                            "transform": "rotate(-90deg)",
                                        },
                                    },
                                },
                            ),
                        ],
                    ),
                    width=3,
                ),
                dbc.Col(
                    html.Div(id="card_content"),
                    width=3,
                ),
            ]
        ),
    ]
)
    return layout
