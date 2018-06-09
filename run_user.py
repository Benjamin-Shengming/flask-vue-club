#!/usr/bin/python3
import dash
from dash.dependencies import Input, State, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

from navibar import nav_bar, nav_bar_links

df = pd.DataFrame({
    'x': [1, 2, 3, 1, 2, 3, 1, 2, 3],
    'y': [3, 2, 4, 1, 4, 5, 4, 3, 1],
    'group-1': ['/', '/exhibit-b', '/exhibit-c', '/', '/exhibit-b', '/exhibit-c', '/', '/exhibit-b', '/exhibit-c'],
    'group-2': ['LA', 'LA', 'LA', 'London', 'London', 'London', 'Montreal', 'Montreal', 'Montreal'],
})


app = dash.Dash()
#app.scripts.config.serve_locally=True

app.config.supress_callback_exceptions = True

# append css
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.css.append_css({"external_url":
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"})
app.scripts.append_script({"external_url":
                    "https://code.jquery.com/jquery-3.2.1.slim.min.js"})
app.scripts.append_script({"external_url":
                    "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"})
app.scripts.append_script({"external_url":
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"})
app.layout = html.Div([
    # This "header" will persist across pages
    nav_bar,

    # This Location component represents the URL bar
    dcc.Location(id='url', refresh=False),

    # Each "page" will modify this element
    html.Div(id='content-container-root'),


], className="container")


@app.callback(
    Output('content-container-root', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/home":
        return "home"
    elif pathname == "/orders":
        return "orders"
    elif  pathname == "/profiles":
        return "orders"



if __name__ == '__main__':
    app.run_server(debug=True)
