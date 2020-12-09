import mydata
import numpy as np
import itertools
from lmts import elw, elw2s, gph, hou_perron, local_w
from plot import candlestick, export_chart

import pandas as pd

# directory path to read data
#
folder_path = 'C:/Users/Ege Yazgan/OneDrive - Istanbul Bilgi Universitesi/BIST_Eylul/eq/'

# Read all data in the specified folder
data = mydata.read_multidir(folder_path)

# Calculate the middle price
data['mid_price'] = (data['bid_price'] + data['ask_price']) / 2

# Create a pivot table using mid price, symbol and time, if two
mid_price = data.pivot_table(index='time', columns='symbol', values='mid_price', aggfunc='mean')

mid_price = mid_price.resample('D').apply(lambda x: x.ffill())

# Convert to 1 minute data for every day (agg func = mean, alternatives: median;...)
mid_price = mid_price.groupby(pd.Grouper(freq='D')).resample('1Min').mean().droplevel(0)

# Calculate natural logarithms
log_mid = np.log(mid_price)

# Pair names
pair_names = list(itertools.combinations(log_mid.columns, 2))

# Calculate the difference of all pairs (435 pair)
all_pairs = list(map(lambda x: (log_mid.loc[:, x[0]] - log_mid.loc[:, x[1]])
                     ._set_name('_'.join(x)), pair_names))

# Remove NaN's
all_pairs = [(lambda x: x.dropna())(pair) for pair in all_pairs]

# pairs concatenate in single df
all_pairs = pd.concat(all_pairs, axis=1)

all_pairs = all_pairs.resample('D').apply(lambda x: x.ffill())

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

# >>>>>> Candlestick >>>>>>>>>
# Get any pair.
akbnk_arclk = all_pairs['AKBNK_ARCLK']

# Create a figure. 'D' describes daily aggregation.
fig = candlestick(akbnk_arclk, 'D')

# Show graph
fig.show()

export_chart(fig, name='akbnk_arclk')
# <<<<<< Candlestick <<<<<<<<<

# Export all charts
for name in all_pairs.columns:
    f = candlestick(all_pairs[name], 'D')
    export_chart(f, name)
