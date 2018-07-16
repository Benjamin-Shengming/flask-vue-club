import dash
import os

from flask import send_from_directory, Flask, request, send_file

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

# create controller object, the central point
from controller import AppController
app_controller = AppController()

class Dash_responsive(dash.Dash):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #Overriding from https://github.com/plotly/dash/blob/master/dash/dash.py#L282
    def index(self, *args, **kwargs):
        scripts = self._generate_scripts_html()
        css = self._generate_css_dist_html()
        config = self._generate_config_html()
        title = getattr(self, 'title', 'Dash')
        return ('''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
                <title>{}</title>
                {}
            </head>
            <body>
                <div id="react-entry-point">
                    <div class="_dash-loading">
                        Loading...
                    </div>
                </div>
            </body>
            <footer>
                {}
                {}
            </footer>
        </html>
        '''.format(title, css, config, scripts))


server = Flask(__name__)



app = Dash_responsive(__name__,
                      server=server,
                      static_folder='assets')

app.config.supress_callback_exceptions = True

app.scripts.config.serve_locally = False


# servce statid files
file_directory = os.path.abspath(os.path.dirname(__name__)) + "/assets"
@server.route('/assets/<path:path>')
def serve_files(path):
    full_file_path = os.path.join(file_directory, path)
    if os.path.exists(full_file_path):
        return send_file(full_file_path)
    else:
        logger.debug("file does not exist {}".format(full_file_path))
        return


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
app.css.append_css({"external_url": "/assets/css/sidebar.css"})

