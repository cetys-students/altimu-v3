import plotly.plotly as plotly
from plotly.graph_objs import Scatter, Layout, Figure
from datetime import datetime

username = 'your_plotly_username'
api_key = 'your_api_key'
stream_token = 'your_stream_token'


class Plotter:

    def __init__(self):
        plotly.sign_in(username, api_key)

        trace = Scatter(
            x=[],
            y=[],
            stream=dict(
                token=stream_token,
                maxpoints=200
            )
        )
        layout = Layout(title='Raspberry Pi Streaming Sensor Data')
        figure = Figure(data=[trace], layout=layout)
        stream = plotly.Stream(stream_token)
        stream.open()

    def plot(self, values):
        self.stream.write({'x': datetime.now(), 'y': values[0]})
