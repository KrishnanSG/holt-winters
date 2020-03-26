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

register_matplotlib_converters()

ts = TimeSeries('dataset/monthly_sales.csv', train_size=0.7)

print("Sales Data\n")
print(ts.data.describe())

print("\nHead and Tail of the time series\n")
print(ts.data.head(5).iloc[:,1:])
print(ts.data.tail(5).iloc[:,1:])

# Plot of raw time series data
plt.plot(ts.data.index,ts.data.sales)
plt.gcf().autofmt_xdate()
date_format = mpld.DateFormatter('%Y-%m')
plt.gca().xaxis.set_major_formatter(date_format)
plt.title("Sales Data Analysis (2013-2016)")
plt.xlabel("Time")
plt.ylabel("Sales")
plt.show()

