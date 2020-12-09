import pandas as pd

BIST30 = ["ARCLK", "ASELS", "BIMAS", "DOHOL", "EKGYO", "FROTO", "HALKB", "GARAN", "ISCTR", "KCHOL", "KOZAA", "KOZAL",
          "KRDMD", "AKBNK", "PETKM", "PGSUS", "SAHOL", "SISE", "EREGL", "SODA", "TAVHL", "TCELL", "THYAO", "TKFEN",
          "TOASO", "TSKB", "TTKOM", "TUPRS", "VAKBN", "YKBNK"]


def download(symbols: list, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Belirtilen BIST kodlarına ait verileri matrix apisini kullanarak alır.

    Args:
        symbols : Bist kodlarını içeren liste.
        start_date : Veri için başlangıç tarihi.
        end_date : Veri için bitiş tarihi.
    Returns:
        DataFrame
    """
    pass


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


def read_multidir(path):
    from os import listdir
    all_paths = map(lambda x: path + x + '/', listdir(path))
    all_data = []
    for _path in all_paths:
        all_data.append(read(_path))
    return pd.concat(all_data)


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


def sample():
    """
    Random verilerle örnek veri seti oluşturur.
    """
    from numpy.random import ranf

    dates = pd.date_range(start='2020-10-01 00:00', end='2020-10-30 00:00', freq='30Min')

    bist_codes = pd.read_csv('data/bist_symbols.csv', squeeze=True)

    data = (ranf(len(dates) * len(bist_codes)) * 10).reshape(len(dates), len(bist_codes))

    return pd.DataFrame(data, index=dates, columns=bist_codes)


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
