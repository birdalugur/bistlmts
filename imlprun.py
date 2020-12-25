import calc
import plotly.express as px
from sklearn.model_selection import train_test_split
import datetime
from importlib import reload

ex_pair = all_pairs['ARCLK_ASELS']
time = datetime.time(12, 0)
dim = 3

low_values = calc.get_ohcl(ex_pair, freq='H', get='low').loc[time].dropna()
high_values = calc.get_ohcl(ex_pair, freq='H', get='high').loc[time].dropna()

train_low, test_low = train_test_split(low_values, shuffle=False, test_size=0.3)
train_high, test_high = train_test_split(high_values, shuffle=False, test_size=0.3)

X_train_low, Y_train_low = calc.to_period(train_low.values.reshape(-1, 1), dim)
X_train_high, Y_train_high = calc.to_period(train_high.values.reshape(-1, 1), dim)

x_test_low, y_test_low = calc.to_period(test_low.values.reshape(-1, 1), dim)
x_test_high, y_test_high = calc.to_period(test_high.values.reshape(-1, 1), dim)

model = imlp.get_model(input_dim=dim, output_dim=1, num_hidden_layers=2, num_units=[200, 200],
                       activation=['relu', 'relu'], beta=0.5)

model.fit(x=[X_train_high, X_train_low], y=[Y_train_high, Y_train_low], epochs=10)

y_pred_high, y_pred_low = model.predict([x_test_high, x_test_low])




from sklearn.metrics import mean_squared_error

# ortalama kare farkı (the best value is 0.0),
loss_high = np.sqrt(mean_squared_error(y_test_high, y_pred_high))

loss_low = np.sqrt(mean_squared_error(y_test_low, y_pred_low))

result = calc_imlp(ex_pair, time, dim)
