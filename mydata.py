import pandas as pd
import pandas.tseries.offsets as offset

BIST30 = ["ARCLK", "ASELS", "BIMAS", "DOHOL", "EKGYO", "FROTO", "HALKB", "GARAN", "ISCTR", "KCHOL", "KOZAA", "KOZAL",
          "KRDMD", "AKBNK", "PETKM", "PGSUS", "SAHOL", "SISE", "EREGL", "SODA", "TAVHL", "TCELL", "THYAO", "TKFEN",
          "TOASO", "TSKB", "TTKOM", "TUPRS", "VAKBN", "YKBNK"]


def is_bist30(x: str) -> bool:
    """
    Is the expression denoted by x a member of bist30?
    """
    for symbol in BIST30:
        if symbol in x:
            return True
    return False


def read(path: str, datecol: str = 'time') -> pd.DataFrame:
    """
    Bir klasörden csv verilerini okuyun.

    Args:
        path : Klasöre ait yol
        datecol : Datetime column. default 'time'.
    """
    from os import listdir

    dt = {'symbol': 'str', 'bid_price': 'float64', 'ask_price': 'float64'}
    path = path + '/eq/'
    all_paths = map(lambda x: path + x, listdir(path))
    all_data = []
    for _path in all_paths:
        if is_bist30(_path):
            try:
                all_data.append(
                    pd.read_csv(_path,
                                dtype=dt,
                                converters={datecol: lambda x: pd.Timestamp(int(x))})
                )
            except pd.errors.EmptyDataError:
                print("Empty Data:\n", _path)

    return pd.concat(all_data)


def read_multidir(path, start_date: str = None, end_date: str = None):
    from os import listdir
    all_paths = map(lambda x: path + x + '/', listdir(path))
    if (start_date is not None) & (end_date is not None):
        all_paths = file_date(list(all_paths), start_date, end_date)
    all_data = []
    for _path in all_paths:
        all_data.append(read(_path))
    return pd.concat(all_data)


def file_date(paths: list, start: str, end: str) -> list:
    """
    paths : list of file paths
    start : '2020-01'
    end : '2020-03'
    """
    date_range = pd.date_range(start, end, freq='MS').to_list()
    date_range = list(map(lambda x: x.strftime('%Y%m'), date_range))
    _paths = pd.Series(paths)
    _paths = _paths[_paths.str.contains('|'.join(date_range))]
    return _paths.to_list()


def time_series(data: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Belirtilen sütundaki değerleri kullanarak zaman serisi oluşturun.

    Args:
        data : Kullanılacak veri.
        col : Değerler için kullanılacak sütun.

    Returns:
        Dataframe: pivot table
    """
    return data.pivot(index='time', columns='symbol', values=col)


def sample(freq='30Min'):
    """
    Random verilerle örnek veri seti oluşturur.
    """
    from numpy.random import ranf

    dates = pd.date_range(start='2020-10-01 00:00', end='2020-10-29 23:00', freq=freq)

    bist_codes = BIST30

    data = (ranf(len(dates) * len(bist_codes)) * 10).reshape(len(dates), len(bist_codes))

    return pd.DataFrame(data, index=dates, columns=bist_codes)


def random_nan(data):
    import numpy as np
    _bools = np.random.randint(0, 2, data.shape) == 1
    data[_bools] = np.nan
    return data


def sort(x):
    return pd.Series(x.sort_values(ascending=False).index, index=range(len(x)))


def intersect(d, percent):
    start = int(len(d.columns) * (100 - percent) / 100)
    end = len(d.columns)
    _slice = d[range(start, end)]
    sets = iter(map(set, _slice.values))
    result = sets.__next__()
    for s in sets:
        result = result.intersection(s)
    return result


def isnull(values) -> bool:
    """
    Check empty data
    """
    if isinstance(values, pd.Series) and values.dropna().size == 0:
        return True
