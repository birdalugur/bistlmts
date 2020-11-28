import pandas as pd

parse_dates = ['date']


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


def read(path: str) -> pd.DataFrame:
    """
    Bir klasörden csv verilerini okuyun.

    Args:
        path : Klasöre ait yol
    """
    from os import listdir

    dt = {'symbol': 'str', 'bid_price': 'float64', 'ask_price': 'float64'}

    all_paths = map(lambda x: path + x, listdir(path))
    all_data = []
    for _path in all_paths:
        try:
            all_data.append(
                pd.read_csv(_path,
                            dtype=dt,
                            converters={'time': lambda x: pd.Timestamp(int(x))})
            )
        except pd.errors.EmptyDataError:
            print("Empty Data:\n", _path)

    return pd.concat(all_data)


#
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
