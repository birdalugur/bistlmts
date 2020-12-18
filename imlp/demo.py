from imlp.imlp import iAct, iLoss, get_model
import numpy as np

# Generate the synthetic data
x1 = np.sin(np.arange(0, 9, 0.01))
x2 = np.cos(np.arange(0, 9, 0.01))
x3 = x1 ** 2
x4 = (x1 + x2) / 2
tmp = np.ones((900,))

Xtrain_c = x3[0:5]
Xtrain_r = tmp[0:5]
Ytrain_c = x4[0:1]
Ytrain_r = tmp[0:1]

for i in range(1, 100):
    Xtrain_c = np.vstack((Xtrain_c, x3[i:i + 5]))
    Xtrain_r = np.vstack((Xtrain_r, tmp[i:i + 5]))
    Ytrain_c = np.vstack((Ytrain_c, x4[i:i + 1]))
    Ytrain_r = np.vstack((Ytrain_r, tmp[i:i + 1]))

Xtrain_c = Xtrain_c[:, 0:2]
Xtrain_r = Xtrain_r[:, 0:2]

pred_values = np.random.randint(1, 10, 200)
pred_values2 = np.random.randint(1, 10, 200)

pred_values1 = pred_values.reshape(100, 2)
pred_values2 = pred_values2.reshape(100, 2)
preds = pred_values1[:, 0:1]

# Parameters
input_dim = 2
output_dim = 1

num_hidden_layers = 2

num_units = [200, 200]

act = ['relu', 'relu']
beta = 0.5

# Get model
model = get_model(input_dim, output_dim, num_units, act, beta, num_hidden_layers)

# Train dim=5
model.fit(x=[Xtrain_c, Xtrain_r], y=[Ytrain_c, Ytrain_r], epochs=10)


model.predict([Xtrain_c, Xtrain_r])


model.predict([pred_values1, pred_values2])
