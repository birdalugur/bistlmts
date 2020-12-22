import pandas as pd
from numpy import nan
import mydata
import datetime


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


def get_ohcl(data: pd.Series, freq: str, get: str) -> pd.DataFrame:
    """
    Get values one of the open, high, low, close from the data in the time interval specified by "freq".

    Args:
        data : numeric pandas series with datetimeindex
        freq : offset value 2H, 5Min..
        get : open, high, low, close
    """
    ohcl_data = data.resample(freq).apply(ohlc)
    _data = ohcl_data.apply(lambda x: x[get])
    date = _data.reset_index()['index'].dt.date
    time = _data.reset_index()['index'].dt.time
    vals = _data.values
    _data = pd.DataFrame({'date': date, 'time': time, 'vals': vals})
    _data = _data.pivot(index='time', columns='date', values='vals')
    return _data


def get_period_data(data: pd.Series) -> pd.DataFrame:
    """
    Get data for the specified time.
    """
    perioddata = data.to_frame(name=data.index.max())
    days = perioddata.index.sort_values(ascending=False)

    for i in range(len(days)):
        if i == len(days) - 1:
            break
        perioddata[days[i + 1]] = perioddata[days[i]].shift()

    return perioddata.sort_index(ascending=False).reset_index(drop=True)


def get_period_data2(data: pd.Series, date) -> pd.DataFrame:
    """
    Get data for the specified time.
    """
    data = data.dropna()
    start = date - datetime.timedelta(len(data) - 1)
    end = date
    days = pd.date_range(start, end, freq='D').sort_values(ascending=False)
    perioddata = data.to_frame(name=days.max()).dropna()

    for i in range(len(days)):
        if i == len(days) - 1:
            break
        perioddata[days[i + 1]] = perioddata[days[i]].shift()

    # perioddata = perioddata.apply(lambda x: x.dropna().reset_index(drop=True))

    return perioddata[::-1]


def to_period(data, timestep=1):
    X, Y = [], []
    for i in range(len(data) - timestep - 1):
        a = data[i:(i + timestep), 0]  # i=0,1,2,3,4,.....
        X.append(a)
        b = data[i + timestep, 0]
        Y.append(b)

    return np.array(X), np.array(Y).reshape(-1, 1)


def get_period(data, time, get):
    low_values = get_ohcl(data, freq='H', get=get)
    low_values = low_values.loc[time]
    low_values = get_period_data(low_values)
    return low_values
