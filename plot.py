import pandas as pd
from numpy import nan
import plotly.graph_objects as go
import mydata


def ohlc(time_series) -> dict:
    """
    Get the open, high, low and close values in the data array.

    Args:
        time_series : (list or pandas series)
    """
    _open, _high, _low, _close = nan, nan, nan, nan

    if mydata.isnull(time_series):
        return {'open': _open, 'high': _high, 'low': _low, 'close': _close}

    if isinstance(time_series, pd.Series):
        _time = time_series.index
        _open = time_series.iloc[0]
        _high = time_series.max()
        _low = time_series.min()
        _close = time_series.iloc[-1]

    elif isinstance(time_series, pd.DataFrame):
        raise ValueError("Use pandas series or python list.")
        # _time = time_series.iloc[:, 0]

    elif isinstance(time_series, list):
        _open = time_series[0]
        _high = max(time_series)
        _low = min(time_series)
        _close = time_series[-1]

    return {'open': _open, 'high': _high, 'low': _low, 'close': _close}


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
