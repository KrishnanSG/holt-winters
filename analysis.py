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

result_add = seasonal_decompose(ts.data.iloc[:,1], period=12, model='additive')
result_add.plot()
plt.gcf().autofmt_xdate()
date_format = mpld.DateFormatter('%y-%m')
plt.gca().xaxis.set_major_formatter(date_format)

result_mul = seasonal_decompose(ts.data.iloc[:,1], period=12, model='multiplicative')
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
model = ExponentialSmoothing(ts.train,trend='additive',seasonal='additive',seasonal_periods=12).fit()
plt.plot(ts.train.index,ts.train,label="Train")
plt.plot(ts.test.index,ts.test,label="Actual")

# Create a 5 year forecast
plt.plot(model.forecast(60),label="Forecast")

plt.legend(['Train','Actual','Forecast'])
plt.gcf().autofmt_xdate()
date_format = mpld.DateFormatter('%Y-%m')
plt.gca().xaxis.set_major_formatter(date_format)
plt.title("Sales Data Analysis (2013-2016)")
plt.xlabel("Time")
plt.ylabel("Sales (x1000)")
plt.show()
