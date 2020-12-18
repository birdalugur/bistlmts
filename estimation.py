import itertools
import numpy as np
import pandas as pd
import datetime

import mydata
from lmts import elw, elw2s, gph, hou_perron, local_w
from plot import candlestick, export_chart, time_series
from calc import get_ohcl, get_period_data
from imlp import imlp

# directory path to read data
folder_path = 'data/shared/tob_changes_bist/'

# Read all data in the specified folder
data = mydata.read_multidir(folder_path, start_date='2020-01', end_date='2020-03')

# Calculate the middle price
data['mid_price'] = (data['bid_price'] + data['ask_price']) / 2

# Create a pivot table using mid price, symbol and time, if two
mid_price = data.pivot_table(index='time', columns='symbol', values='mid_price', aggfunc='mean')

mid_price = mid_price.resample('D').apply(lambda x: x.ffill())

# Convert to 1 minute data for every day (agg func = mean, alternatives: median;...)
mid_price = mid_price.groupby(pd.Grouper(freq='D')).resample('1Min').mean().droplevel(0)

# Calculate natural logarithms
log_mid = np.log(mid_price)

log_mid = mydata.sample(freq='1Min')

# Pair names
pair_names = list(itertools.combinations(log_mid.columns, 2))

# Calculate the difference of all pairs (435 pair)
all_pairs = list(map(lambda x: (log_mid.loc[:, x[0]] - log_mid.loc[:, x[1]])
                     ._set_name('_'.join(x)), pair_names))

# Remove NaN's
all_pairs = [(lambda x: x.dropna())(pair) for pair in all_pairs]

# pairs concatenate in single df
all_pairs = pd.concat(all_pairs, axis=1)

# fill nan values (ignore end of the day)
all_pairs = all_pairs.resample('D').apply(lambda x: x.apply(lambda x: x[:x.last_valid_index()].ffill()))
all_pairs = all_pairs.droplevel(0)

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

# Time Series Chart
fig = time_series(akbnk_arclk, 'last', '1H')
fig.show()

# Export all charts
for name in all_pairs.columns:
    # f = candlestick(all_pairs[name], 'D')
    f = time_series(all_pairs[name], 'last', '1H')
    export_chart(f, name)

# >>>>>> impl estimation >>>>>>>>>

ex_pair = all_pairs['ARCLK_ASELS']

low_values = get_ohcl(ex_pair, freq='H', get='low')
high_values = get_ohcl(ex_pair, freq='H', get='high')

time = datetime.time(0, 0)


zero_low = get_period_data(low_values, time)
zero_high = get_period_data(high_values,time)


model = imlp.get_model(input_dim=5, output_dim=1, num_hidden_layers=2, num_units=[200, 200],
                       activation=['relu', 'relu'], beta=0.5)

current_date = datetime.datetime(2020, 10, 29).date()

current_low = low_values[current_date]
current_high = high_values[current_date]

previous_high = high_values.iloc[:, 1:6]
previous_low = low_values.iloc[:, 1:6]

model.fit(x=[previous_high, previous_low], y=[current_high, current_low], epochs=10)

pred_high = high_values.iloc[:, 7:12]
pred_low = low_values.iloc[:, 7:12]

model.predict([pred_high, pred_low])

# <<<<<< impl estimation <<<<<<<<<
