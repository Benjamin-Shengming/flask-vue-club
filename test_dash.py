#!/usr/bin/python3
import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
from uuid import uuid1
app = dash.Dash()

app.config.supress_callback_exceptions = True

class BaseBlock:
    def __init__(self, app=None):
        self.app = app

        if self.app is not None and hasattr(self, 'callbacks'):
            self.callbacks(self.app)

class MyBlock(BaseBlock):
    def __init__(self, app=None):
        self.id1 = str(uuid1())
        self.id2 = str(uuid1())
        self.id3= str(uuid1())
        self.id4= str(uuid1())
        super(MyBlock, self).__init__(app=app)
        self.layout = html.Div(id='layout for this "block".', children=[
            dcc.Input(id=self.id1),
            dcc.Input(id=self.id2),
            dcc.Input(id=self.id3),
            dcc.Input(id=self.id4)
        ])

    def callbacks(self, app):

        @app.callback(Output(self.id1, 'value'), [Input(self.id2, 'value')])
        def do_things(bar):
            return bar

        @app.callback(Output(self.id3, 'value'), [Input(self.id4, 'value')])
        def do_things(boop):
            return boop

# creating a new MyBlock will register all callbacks
block = MyBlock(app=app)
block1 = MyBlock(app=app)
# now insert this component into the app's layout
app.layout = html.Div(children=[block.layout, block1.layout])
if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
