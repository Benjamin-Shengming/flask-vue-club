import dash
import os

from flask import send_from_directory, Flask, request, send_file

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

# create controller object, the central point
from controller import AppController
app_controller = AppController()

server = Flask(__name__)


external_scripts = [
    "https://code.jquery.com/jquery-3.2.1.slim.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
]

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css",
    "https://use.fontawesome.com/releases/v5.1.0/css/all.css",
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
]


app = dash.Dash(__name__,
                server=server,
                static_folder='assets',
                meta_tags=[
                    {
                        "name": "viewport",
                        "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
                    }
                ],
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets
               )

app.config.supress_callback_exceptions = True
app.scripts.config.serve_locally = False


# serve static files
file_directory = os.path.abspath(os.path.dirname(__name__)) + "/assets"
@server.route('/assets/<path:path>')
def serve_files(path):
    logger.debug("request file " + path)
    full_file_path = os.path.join(file_directory, path)
    if os.path.exists(full_file_path):
        return send_file(full_file_path)
    else:
        logger.debug("file does not exist {}".format(full_file_path))
        return
