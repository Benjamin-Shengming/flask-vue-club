import dash
import os

from flask import send_from_directory


# create controller object, the central point
from controller import AppController
app_controller = AppController()

app = dash.Dash(__name__, static_folder='assets')
server = app.server
app.config.supress_callback_exceptions = True

app.scripts.config.serve_locally = False

# css logical
css_directory = os.path.dirname(__name__) + "/assets/css/"
stylesheets_local =  ['sidebar.css']   # local style sheet need to use
def serve_stylesheet(stylesheet):
    if stylesheet not in stylesheets_local:
        raise Exception(
                    '"{}" is excluded from the allowed static files'.format(
                        stylesheet
                    )
                )
    return flask.send_from_directory(css_directory, stylesheet)

external_css = [
]
for css in external_css:
    app.css.append_css({"external_url": css})

app.css.append_css({"external_url":
                    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css"})

app.css.append_css({"external_url":
                    "https://use.fontawesome.com/releases/v5.1.0/css/all.css"})

app.css.append_css({"external_url":
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"})
app.scripts.append_script({"external_url":
                    "https://code.jquery.com/jquery-3.2.1.slim.min.js"})
app.scripts.append_script({"external_url":
                    "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"})
app.scripts.append_script({"external_url":
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"})
# append local css
for stylesheet in stylesheets_local:
    app.css.append_css({"external_url": "/assets/css/{}".format(stylesheet)})

