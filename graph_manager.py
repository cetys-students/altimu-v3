import plotly.exceptions as py_exceptions
import plotly.graph_objs as go
import plotly.plotly as py


class GraphManager:
    """This class implements a wrapper around plotly. To create a plotly chart, create an instance
    of this class, call add_data_set for each plot you want to add, and call show to display
    the chart in the browser."""

    def __init__(self, graph_title: str, x_axis_label: str):
        self.graph_title = graph_title
        self.x_axis_label = x_axis_label
        self.layout = go.Layout(title=graph_title, xaxis={'title': x_axis_label})
        self.plots = []

    # For a list of allowable plotly marker symbols, see
    # https://plot.ly/python/reference/#scatter.

    def add_data_set(self, *, name: str, x_values: [int] = None, y_values: [float],
                     color: str = 'black', dash: str = 'none'):
        if x_values is None:
            x_values = list(range(0, len(y_values)))

        plot = go.Scatter(name=name, x=x_values, y=y_values,
                          mode='lines',
                          hoverinfo='x+y',
                          line={
                              'color': color,
                              'dash': dash
                          })
        self.plots.append(plot)

    def show(self):
        try:
            figure = go.Figure(data=self.plots, layout=self.layout)
            py.plot(figure, file_name=self.graph_title)
        except py_exceptions.PlotlyError as e:
            print('***ERROR: Cannot print chart.')
            print(e)
