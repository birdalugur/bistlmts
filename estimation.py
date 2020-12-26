import itertools
import numpy as np
import pandas as pd
import datetime
from os.path import isdir
from os import mkdir

import mydata
from lmts import elw, elw2s, gph, hou_perron, local_w
from plot import candlestick, export_chart, time_series
from calc import get_ohcl, get_period_data, residuals
from imlp import imlp

# directory path to read data
folder_path = 'data/BIST_Eylul/'

# Read all data in the specified folder
data = mydata.read_multidir(folder_path, start_date='2020-01', end_date='2020-03')

# data = mydata.read(folder_path)

# Calculate the middle price
data['mid_price'] = (data['bid_price'] + data['ask_price']) / 2

# Create a pivot table using mid price, symbol and time, if two
mid_price = data.pivot_table(index='time', columns='symbol', values='mid_price', aggfunc='mean')

# Convert to 1 minute data for every day (agg func = mean, alternatives: median;...)
mid_price = mid_price.groupby(pd.Grouper(freq='D')).resample('1Min').mean().droplevel(0)

# fill nan values (ignore end of the day)
mid_price = mid_price.resample('D').apply(lambda x: x.apply(lambda x: x[:x.last_valid_index()].ffill()))
mid_price = mid_price.droplevel(0)

# Pair names
pair_names = list(itertools.combinations(mid_price.columns, 2))

# Residuals
all_pairs = pd.concat(
    [residuals(mid_price[first], mid_price[second]) for first, second in pair_names], axis=1
).set_index(mid_price.index)

# Calculate natural logarithms
log_mid = np.log(mid_price)

# Calculate the difference of all pairs (435 pair)
all_pairs = list(map(lambda x: (log_mid.loc[:, x[0]] - log_mid.loc[:, x[1]])
                     ._set_name('_'.join(x)), pair_names))

# pairs concatenate in single df
all_pairs = pd.concat(all_pairs, axis=1)

# write results to csv
if not isdir('output'):
    mkdir('output')
all_pairs.to_csv('output/all_pairs.csv')

# >>>>>> estimation >>>>>>>>>
elw_data = all_pairs.resample('D').apply(elw)
elw2s_data = all_pairs.resample('D').apply(elw2s)
gph_data = all_pairs.resample('D').apply(gph)
hou_perron_data = all_pairs.resample('D').apply(hou_perron)
local_w_data = all_pairs.resample('D').apply(local_w)
# <<<<<< estimation <<<<<<<<<

# Sort the d's in descending order. To sort by day, pass axis=0.
sorted_elw = elw_data.apply(mydata.sort, axis=1)

# intersection of the lowest 10 percent
mydata.intersect(sorted_elw, 10)

# Export all charts
for name in all_pairs.columns:
    # f = candlestick(all_pairs[name], 'D')
    f = time_series(all_pairs[name], 'last', '1H')
    export_chart(f, name)
