import pandas as pd
import plotly.graph_objects as go
import mydata
from calc import ohlc


def candlestick(data, offset='D'):
    ohcl = data.resample(offset).apply(ohlc)
    _time = ohcl.index
    _open, _high, _low, _close = [], [], [], []
    for item in ohcl.values:
        _open.append(item['open'])
        _high.append(item['high'])
        _low.append(item['low'])
        _close.append(item['close'])

    fig = go.Figure(
        data=go.Candlestick(x=_time, open=_open, high=_high, low=_low, close=_close)
    )

    return fig


def export_chart(fig: go.Figure, name: str, location: str = None):
    """
    Save the graphics you created. Results are saved in html format.

    Args:
        fig : Plotly graphic object.
        location : The path to the location. Default it saves in the charts directory.
        name : File name
    """
    from plotly.offline import plot
    from os import mkdir, listdir

    if location is None:
        if 'charts' not in listdir():
            mkdir('charts')
        location = 'charts'

    _path = location + '/' + name + '.html'

    plot(fig, auto_open=False, filename=_path)


def time_series(data, func, offset: str):
    _data = data.resample(offset).apply(func)
    fig = go.Figure()
    time = _data.index
    values = _data.values
    fig.add_trace(go.Scatter(x=time, y=values, mode='lines', name='lines'))
    fig.update_xaxes(rangeslider_visible=True)
    return fig
