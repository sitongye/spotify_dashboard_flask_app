from dash import html
import dash_bootstrap_components as dbc

navbar = html.Div([
    dbc.NavbarSimple(
        brand="My Dash App",
        brand_href="#",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="#")),
            dbc.NavItem(dbc.NavLink("About", href="#")),
            dbc.NavItem(dbc.NavLink("Contact", href="#")),
        ],
    )
])

footer = html.Footer(
    html.Div(
        dbc.Container(
            dbc.Row(
                dbc.Col(
                    html.P("© 2023 Spotify AB"),
                ),
            ),
        ),
    ),
)

def BaseLayout(content):
    return html.Div([
        html.Header([
            html.Title("My Dash App"),
            html.Meta(charSet="UTF-8"),
            html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            html.Link(rel="stylesheet", href=dbc.themes.BOOTSTRAP),
            html.Link(rel="stylesheet", href="/static/css/styles.css"),
            html.Div(id="stylesheet"),
        ]),
        navbar,
        dbc.Container([
            html.Main([
                content,
            ]),
        ], fluid=True, className="mt-4"),
        html.Script(src="https://code.jquery.com/jquery-3.6.4.slim.min.js", integrity="sha256-a2yjHM4jnF9f54xUQakjZGaqYs/V1CYvWpoqZzC2/Bw=", crossOrigin="anonymous"),
        html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.10.2/umd/popper.min.js", integrity="sha512-nnzkI2u2Dy6HMnzMIkh7CPd1KX445z38XIu4jG1jGw7x5tSL3VBjE44dY4ihMU1ijAQV930SPM12cCFrB18sVw==", crossOrigin="anonymous", referrerPolicy="no-referrer"),
        html.Script(src="/static/js/bootstrap.min.js"),
        footer,
    ])