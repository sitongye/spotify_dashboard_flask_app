from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

navbar = dbc.NavbarSimple(
    brand="Spotify",
    fixed="top",
    brand_href="#",
    color="primary",
    dark=True,
    brand_style={"fontSize": "24px", "fontWeight": "bold", "LineHeight": "1.5"},
    style={
        "height": "10%",
        "lineHeight": "1.5",
        "fontSize": "16px",
        "TextAlign": "left",
        "FontWeight": "400",
        "AlignItem": "center",
    },
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#", style={"padding": "15px"})),
        dbc.NavItem(dbc.NavLink("About", href="#", style={"padding": "15px"})),
        dbc.NavItem(dbc.NavLink("Contact", href="#", style={"padding": "15px"})),
    ],
)

footer = dmc.Footer(
    height="5%",
    fixed=True,
    children=[
        dmc.Text(
            "© 2023 Sitong Ye",
            style={"fontFamily": "'Helvetica Neue', Helvetica, Arial, sans-serif"},
        )
    ],
    style={"backgroundColor": "#121212", "textAlign": "center", "borderTopWidth": "0"},
)


def BaseLayout(content):

    return html.Div(
        [
            html.Header(
                [
                    html.Meta(charSet="UTF-8"),
                    html.Meta(
                        name="viewport", content="width=device-width, initial-scale=1.0"
                    ),
                ]
            ),
            navbar,
            html.Div(content, style={"marginTop":"10%"}),
            footer,
        ]
    )
