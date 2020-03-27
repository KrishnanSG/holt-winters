"""
Anomaly Detection using Brutlag algorithm
-----------------------------------------
This file contains the implementation brutlag algorithm and it can be used to detect anomalies
in time series data.

Dataset
-------
The dataset contains India's monthly average temperature (°C) recorded for a period of 2000-2018.
"""

from time_series import TimeSeries

# Holt-Winters or Triple Exponential Smoothing model
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Imports for data visualization
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from matplotlib import dates as mpld

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

ts = TimeSeries('dataset/average_temp_india.csv', train_size=0.7)

plt.plot(ts.data.iloc[:,1].index,ts.data.iloc[:,1])
plt.gcf().autofmt_xdate()
plt.title("Average Temperature of India (2000-2018)")
plt.xlabel("Time")
plt.ylabel("Temparature (°C)")
plt.show()

model = ExponentialSmoothing(
    ts.train, trend='additive', seasonal='additive').fit()
prediction = model.predict(
    start=ts.data.iloc[:, 1].index[0], end=ts.data.iloc[:, 1].index[-1])

"""Brutlag Algorithm"""
PERIOD = 12        # The given time series has seasonal_period=12
GAMMA = 0.3684211  # the seasonility component
SF = 1.96          # brutlag scaling factor for the confidence bands.
UB = []            # upper bound or upper confidence band
LB = []            # lower bound or lower confidence band

difference_array = []
dt = []
difference_table = {
    "actual": ts.data.iloc[:, 1], "predicted": prediction, "difference": difference_array, "UB": UB, "LB": LB}

"""Calculatation of confidence bands using brutlag algorithm"""
for i in range(len(prediction)):
    diff = ts.data.iloc[:, 1][i]-prediction[i]
    if i < PERIOD:
        dt.append(GAMMA*abs(diff))
    else:
        dt.append(GAMMA*abs(diff) + (1-GAMMA)*dt[i-PERIOD])

    difference_array.append(diff)
    UB.append(prediction[i]+SF*dt[i])
    LB.append(prediction[i]-SF*dt[i])

print("\nDifference between actual and predicted\n")
difference = pd.DataFrame(difference_table)
print(difference)

"""Classification of data points as either normal or anomaly"""
normal = []
normal_date = []
anomaly = []
anomaly_date = []

for i in range(len(ts.data.iloc[:, 1].index)):
    if (UB[i] <= ts.data.iloc[:, 1][i] or LB[i] >= ts.data.iloc[:, 1][i]) and i > PERIOD:
        anomaly_date.append(ts.data.index[i])
        anomaly.append(ts.data.iloc[:, 1][i])
    else:
        normal_date.append(ts.data.index[i])
        normal.append(ts.data.iloc[:, 1][i])

anomaly = pd.DataFrame({"date": anomaly_date, "value": anomaly})
anomaly.set_index('date', inplace=True)
normal = pd.DataFrame({"date": normal_date, "value": normal})
normal.set_index('date', inplace=True)

print("\nThe data points classified as anomaly\n")
print(anomaly)

"""
Plotting the data points after classification as anomaly/normal.
Data points classified as anomaly are represented in red and normal in green.
"""
plt.plot(normal.index, normal, 'o', color='green')
plt.plot(anomaly.index, anomaly, 'o', color='red')

# Ploting brutlag confidence bands
plt.plot(ts.data.iloc[:, 1].index, UB, linestyle='--', color='grey')
plt.plot(ts.data.iloc[:, 1].index, LB, linestyle='--', color='grey')

# Formatting the graph
plt.legend(['Normal', 'Anomaly', 'Upper Bound', 'Lower Bound'])
plt.gcf().autofmt_xdate()
plt.title("Average Temperature of India (2000-2018)")
plt.xlabel("Time")
plt.ylabel("Temparature (°C)")
plt.show()
