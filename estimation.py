import mydata
import numpy as np
import itertools
from lmts import elw, elw2s, gph, hou_perron, local_w

import pandas as pd
from pandas import offsets

# directory path to read data
folder_path = 'data/'

# Read all data in the specified folder
data = mydata.read(folder_path)

# Calculate the middle price
data['mid_price'] = (data['bid_price'] + data['ask_price']) / 2

# Create a pivot table using mid price, symbol and time
mid_price = data.pivot_table(index='time', columns='symbol', values='mid_price', aggfunc='mean')

# Convert to 1 minute data for every day (agg func = mean)
mid_price = mid_price.groupby(pd.Grouper(freq='D')).resample('1Min').mean().droplevel(0)

# Calculate natural logarithms
log_mid = np.log(mid_price)

# Example data for test
exdata = (log_mid + 2 ** np.e).set_index(log_mid.index + offsets.Day())
exdata + exdata.shift()
log_mid = pd.concat([log_mid, exdata])

# Pair names
pair_names = list(itertools.combinations(log_mid.columns, 2))

# Calculate the difference of all pairs (435 pair)
all_pairs = list(map(lambda x: (log_mid.loc[:, x[0]] - log_mid.loc[:, x[1]])
                     ._set_name('_'.join(x)), pair_names))

# Remove NaN's
all_pairs = [(lambda x: x.dropna())(pair) for pair in all_pairs]

# pairs concatenate in single df
all_pairs = pd.concat(all_pairs, axis=1)

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
