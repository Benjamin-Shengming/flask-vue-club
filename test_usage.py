import local_storage
import dash
import dash_html_components as html

app = dash.Dash('')

app.scripts.config.serve_locally = True

app.layout = html.Div([
    local_storage.LocalStorageComponent(
        id='input', label="key1"
    ),
    html.Button(id='test-button'),
    html.Div("click me", id='output')
])

@app.callback(
	dash.dependencies.Output('input', 'value'),
	[dash.dependencies.Input('test-button', 'n_clicks')],
    [dash.dependencies.State('input', 'value')])
def display_output(value, pre_value):
    if not value or value <= 0:
        raise ValueError("Do nothing")
    print(pre_value)
    print(value)
    return str(int(pre_value) + 1)

if __name__ == '__main__':
    app.run_server(debug=True)
