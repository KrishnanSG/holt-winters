"""
Analysis of Sales data

Dataset
-------
The given dataset contains monthly total sales of a company for the period 2013-2016.

Ojectives
---------
1. To analyse the sales and understand the performance of the company.
2. Find patterns and construct a model to forecast future sales.
"""
from time_series import TimeSeries

# Imports for data visualization
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import DateFormatter
from matplotlib import dates as mpld

# Seasonal Decompose
from statsmodels.tsa.seasonal import seasonal_decompose

# Holt-Winters or Triple Expoenntial Smoothing model
from statsmodels.tsa.holtwinters import ExponentialSmoothing

register_matplotlib_converters()

ts = TimeSeries('dataset/monthly_sales.csv', train_size=0.8)

print("Sales Data\n")
print(ts.data.describe())

print("\nHead and Tail of the time series\n")
print(ts.data.head(5).iloc[:, 1:])
print(ts.data.tail(5).iloc[:, 1:])

# Plot of raw time series data
plt.plot(ts.data.index, ts.data.sales)
plt.gcf().autofmt_xdate()
date_format = mpld.DateFormatter('%Y-%m')
plt.gca().xaxis.set_major_formatter(date_format)
plt.title("Sales Data Analysis (2013-2016)")
plt.xlabel("Time")
plt.ylabel("Sales")

"""
Seasonal Decompose of the time series
-------------------------------------
Seasonal decompose is a method used to decompose the components of a time series into the following:
- Level - average value in the series.
- Trend - increasing or decreasing value in the series.
- Seasonality - repeating short-term cycle in the series.
- Noise - random variation in the series.

The analysis of the components individually provide better insights for model selection.
"""

result_add = seasonal_decompose(
    ts.data.iloc[:, 1], period=12, model='additive')
result_add.plot()
plt.gcf().autofmt_xdate()
date_format = mpld.DateFormatter('%y-%m')
plt.gca().xaxis.set_major_formatter(date_format)

result_mul = seasonal_decompose(
    ts.data.iloc[:, 1], period=12, model='multiplicative')
result_mul.plot()
plt.gcf().autofmt_xdate()
date_format = mpld.DateFormatter('%y-%m')
plt.gca().xaxis.set_major_formatter(date_format)
plt.show()

"""
Observation from Seasonal Decompose
-----------------------------------
1. The time series seems to roughly have a constant seasonality but has an overall **increasing trend**
2. The slight descreasing trend is observed till 2014-07 after that an increasing trend is observed.

Model Selection
---------------
From the above observation we can evidently conclude that **Holt-Winter additive model** would be an 
appropriate choice as there is a constant seasonality component along with an increasing trend.
"""
# Scaling down the data by a factor of 1000
ts.set_scale(1000)

# Training the model
model = ExponentialSmoothing(ts.train, trend='additive',
                             seasonal='additive', seasonal_periods=12).fit(damping_slope=1)
plt.plot(ts.train.index, ts.train, label="Train")
plt.plot(ts.test.index, ts.test, label="Actual")

# Create a 5 year forecast
plt.plot(model.forecast(60), label="Forecast")

plt.legend(['Train', 'Actual', 'Forecast'])
plt.gcf().autofmt_xdate()
date_format = mpld.DateFormatter('%Y-%m')
plt.gca().xaxis.set_major_formatter(date_format)
plt.title("Sales Data Analysis (2013-2016)")
plt.xlabel("Time")
plt.ylabel("Sales (x1000)")
plt.show()


"""
Validation of the model
-----------------------
Lets do a brief comparison between additive and multiplicative model
"""

ts = TimeSeries('dataset/monthly_sales.csv', train_size=0.8)

# Additive model
model_add = ExponentialSmoothing(
    ts.data.iloc[:, 1], trend='additive', seasonal='additive', seasonal_periods=12, damped=True).fit(damping_slope=0.98)
prediction = model_add.predict(
    start=ts.data.iloc[:, 1].index[0], end=ts.data.iloc[:, 1].index[-1])
plt.plot(ts.data.iloc[:, 1].index, ts.data.iloc[:, 1], label="Train")
plt.plot(ts.data.iloc[:, 1].index, prediction, label="Model")
plt.plot(model_add.forecast(60))

plt.legend(['Actual', 'Model', 'Forecast'])
plt.gcf().autofmt_xdate()
date_format = mpld.DateFormatter('%Y-%m')
plt.gca().xaxis.set_major_formatter(date_format)
plt.title("Sales Data Analysis (2013-2016)")
plt.xlabel("Time")
plt.ylabel("Sales (x1000)")
plt.show()


# Multiplicative model
model_mul = ExponentialSmoothing(
    ts.data.iloc[:, 1], trend='additive', seasonal='multiplicative', seasonal_periods=12, damped=True).fit()
prediction = model_mul.predict(
    start=ts.data.iloc[:, 1].index[0], end=ts.data.iloc[:, 1].index[-1])
plt.plot(ts.data.iloc[:, 1].index, ts.data.iloc[:, 1], label="Train")
plt.plot(ts.data.iloc[:, 1].index, prediction, label="Model")
plt.plot(model_mul.forecast(60))
plt.legend(['Actual', 'Model', 'Forecast'])
plt.gcf().autofmt_xdate()
date_format = mpld.DateFormatter('%Y-%m')
plt.gca().xaxis.set_major_formatter(date_format)
plt.title("Sales Data Analysis (2013-2016)")
plt.xlabel("Time")
plt.ylabel("Sales (x1000)")
plt.show()

print(model_add.summary())
print(model_mul.summary())


"""
Conclusion of the analysis
--------------------------
From the model summary obtained its clear that sum of squared errors (SSE) for 
additive (5088109579.122) < SSE for multiplicative(5235252441.242).

Hence the initial assumption that seasonality is roughly constant and therefore 
choosing additive model was appropriate.

Note: The forecast made using multiplicative model seems to be unrealistic since 
the variance between the high and low on an average is 100000 which is somewhat 
unexpected in real world sales compared to 63000 incase of additive model.
"""
