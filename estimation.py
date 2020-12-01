import webbrowser
import mydata
import numpy as np
import itertools
from rpy2.robjects.packages import importr
from rpy2 import robjects
from math import floor
import pandas as pd

# Open the LongMemoryTS package documentation page.
webbrowser.open('https://www.rdocumentation.org/packages/LongMemoryTS/versions/0.1.0')

# Create lmts object
lmts = importr('LongMemoryTS')

# directory path to read data
folder_path = 'data/'

# Read all data in the specified folder
data = mydata.read(folder_path)

# Calculate the middle price
data['mid_price'] = (data['bid_price'] + data['ask_price']) / 2

# Create a pivot table using mid price, symbol and time
mid_price = data.pivot_table(index='time', columns='symbol', values='mid_price', aggfunc='mean')

# Convert to 1 minute data for every day (agg func = mean)
mid_price = mid_price.groupby([pd.Grouper(freq='D'), pd.Grouper(freq='1Min')]).mean()

# Calculate natural logarithms
log_mid = np.log(mid_price)

# Create all pairs
log_mid = [(lambda x: log_mid.loc[:, x])(pair) for pair in itertools.combinations(log_mid.columns, 2)]

# calculate pair diff
log_mid = map(lambda x: (x.iloc[:, 0] - x.iloc[:, 1])._set_name('_'.join(x.columns)), log_mid)

# Remove NaN's
log_mid = [(lambda x: x.dropna().values)(pair) for pair in log_mid]

# Converting to r objects
r_vectors = list(map(robjects.FloatVector, log_mid))

# >>>>>> estimation functions >>>>>>>>>
# parameters can be changed as specified in the documentation
elw = [lmts.ELW(vector, **{'m': floor(1 + len(vector) ** 0.6), 'mean.est': "mean"})[0][0] for vector in r_vectors]

# TODO: @taper parametresi 'Velasco' olarak atandığında hata alınır.
elw2s = [lmts.ELW2S(vector, **{'m': floor(1 + len(vector) ** 0.6), 'trend_order': 1, 'taper': 'HC'})[0][0] for vector in
         r_vectors]

gph = [lmts.gph(vector, **{'m': floor(1 + len(vector) ** 0.6), 'l': 1})[0] for vector in r_vectors]

hou_perron = [lmts.Hou_Perron(vector, **{'m': floor(1 + len(vector) ** 0.6)})[0][0] for vector in r_vectors]

# TODO: @taper parametresi 'Velasco' olarak atandığında hata alınır.
local_w = [lmts.local_W(vector,
                        **{'int': robjects.FloatVector([-0.5, 2.5]), 'm': floor(1 + len(vector) ** 0.6),
                           'diff_param': 1,
                           'taper': 'HC', 'l': 1})[0][0] for vector in r_vectors]

# <<<<<< estimation functions <<<<<<<<<


pair_names = ['_'.join(pair) for pair in itertools.combinations(mid_price.columns, 2)]

estimation = pd.DataFrame(data={'elw': elw, 'elw2s': elw2s, 'gph': gph, 'hou_perron': hou_perron}, index=pair_names)

estimation.to_csv('estimation.csv')
