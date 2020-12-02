import webbrowser
from math import floor

from rpy2 import robjects
from rpy2.robjects.packages import importr

# Open the LongMemoryTS package documentation page.
webbrowser.open('https://www.rdocumentation.org/packages/LongMemoryTS/versions/0.1.0')

# Create lmts object
lmts = importr('LongMemoryTS')


def convert_Rvectors(values):
    """
    Converts python array to r vector. If any, NaN values are removed.
    """
    values = values.dropna()
    vector = robjects.FloatVector(values)
    return vector


# >>>>>> estimation functions >>>>>>>>>


def elw(values):
    """
    parameters can be changed as specified in the documentation
    """
    vector = convert_Rvectors(values)
    _elw = lmts.ELW(vector, **{'m': floor(1 + len(vector) ** 0.6), 'mean.est': "mean"})[0][0]
    return _elw


def elw2s(values):
    # TODO: @taper parametresi 'Velasco' olarak atandığında hata alınır.
    vector = convert_Rvectors(values)
    _elw2s = lmts.ELW2S(vector, **{'m': floor(1 + len(vector) ** 0.6), 'trend_order': 1, 'taper': 'HC'})[0][0]
    return _elw2s


def gph(values):
    vector = convert_Rvectors(values)
    _gph = lmts.gph(vector, **{'m': floor(1 + len(vector) ** 0.6), 'l': 1})[0]
    return _gph


def hou_perron(values):
    vector = convert_Rvectors(values)
    _hou_perron = lmts.Hou_Perron(vector, **{'m': floor(1 + len(vector) ** 0.6)})[0][0]
    return _hou_perron


def local_w(values):
    # TODO: @taper parametresi 'Velasco' olarak atandığında hata alınır.
    vector = convert_Rvectors(values)
    _local_w = lmts.local_W(vector,
                            **{'int': robjects.FloatVector([-0.5, 2.5]), 'm': floor(1 + len(vector) ** 0.6),
                               'diff_param': 1,
                               'taper': 'HC', 'l': 1})[0][0]
    return _local_w

# <<<<<< estimation functions <<<<<<<<<
