"""
This file holds the interface for the data streaming interface.
"""

import datetime as dt
from dash import Dash, dcc, html, Input, Output
from src.classes.heat_pump import HeatPump


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

""" -------------------
Object creation
------------------------ """

heat_pump = HeatPump(
    t_set=19,
    t_range=0.5,
    p_compressor=2,
    demo_mode=True
)

# Demo data
x_start = heat_pump.connection.state.timestamp
y_start = heat_pump.connection.state.t_inside
figure = dict(
    data=[{'x': [x_start], 'y': [y_start]}],
    layout=dict(xaxis=dict(range=[x_start, x_start + dt.timedelta(minutes=5)]),
                yaxis=dict(range=[15, 23])))


app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(['LA', 'NYC', 'MTL'],
                 'LA',
                 id='dropdown'
                 ),
    html.Div(id='display-value'),
    html.Div(
        dcc.Input(
                id="input_tado_email",
                type='email',
                placeholder="input type email",
        )
    ),
    html.Div(
        dcc.Input(
            id="input_tado_password",
            type='password',
            placeholder="input type password",
        )
    ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit'),

    dcc.Graph(id='graph', figure=figure),
    dcc.Interval(
        id='interval-component',
        interval=3 * 1000,  # in milliseconds
        n_intervals=0
    )
])





@app.callback(
    Output('graph', 'extendData'),
    [Input('interval-component', 'n_intervals')])
def update_data(n_intervals):
    heat_pump.get_current_state()

    x_data = heat_pump.connection.state.timestamp
    y_point = heat_pump.connection.state.t_inside

    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[x_data]], y=[[y_point]]), [0], 1000


""" -------------------------
Callbacks
------------------------- """

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks')
)
def update_output(n_clicks):
    heat_pump.get_current_state()
    return 'The input value was unkonwn and the button has been clicked {} times'.format(

        round(heat_pump.connection.state.t_inside, 2)
    )

@server.route('/greet')
def say_hello():
    return 'Hello from Server'


@app.callback(Output('display-value', 'children'),
              [Input('dropdown', 'value')])
def display_value(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)
