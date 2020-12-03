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

