# Holt-Winters Forecasting 

# Table of Contents
[TOC]

# Introduction
Holt-Winters forecasting is a way to model and predict the behavior of a sequence of values over time—a time series.


# Mathematical Overview
Before getting into the analysis of the real-time series model let's understand a few basic concepts required to have a deeper understanding of the topic.

## Time Series
A time series is a sequence of numerical data points in successive and chronological order. Generally, the x-axis or index is taken as time and the y-axis or value represents the value for the corresponding x value.

### Aspects of Time Series
1. Level - the typical value  or the average 
2. Trend - the slope at that instance 
3. Seasonality - cyclical repeating pattern

## Exponential Smoothing
Before knowing what is exponential smoothing lets understand why it's required.

### Why exponential smoothing?
The real-world datasets for time series are hard to forecast and generally, it's assumed that data of recent past have higher significance compared to old data, hence more weightage is given to recent data than older data.

The problem faced with [weighted moving average](https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/wma) is choosing the appropriate weights for each level.


Exponential smoothing uses EWMA (Exponential Weighted Moving Average), i.e older data have lesser contribution compared to newer data. In EWMA weights reduce exponentially overtime and provide reasonable weights for each level.

### Formula
If you have some time series xt, you can define a new time series st that is a smoothed version of xt.

![](https://latex.codecogs.com/svg.latex?s_t%3D%20%5Calpha%20x_t%20&plus;%20%281-%20%5Calpha%29s_t_-_1)

The following graph with α=0.5 shows how weights of older data diminish over time. The black bars denote the actual value(xt) and colored bars denote the smoothened value(st).

![](https://www.vividcortex.com/hubfs/Blog/Exponentially_Weighted_Moving_4.png)

[Image Source](https://www.vividcortex.com/blog/2014/11/25/how-exponentially-weighted-moving-averages-work/)

## Holt's Model

Holt's model or Double Exponential Smoothing is an extension to simple exponential smoothing.

### Drawbacks of SES
- SES assumes the time series to be [stationary](https://otexts.com/fpp2/stationarity.html),i.e it assume the statistical properties such as the mean, variance and autocorrelation are all constant over time.
- But in general a majority of time series dataset have either trend or seasonality component, thus forecasts made by SES are unproductive.


### What is Holt's Model?
Holt's model overcomes the drawback of SES by considering both level and trend commponent. The term **double exponential smoothing** was coined because exponential smoothing is performed both on level and trend component.

### Formula

![](https://latex.codecogs.com/svg.latex?F_t_&plus;_1%20%3D%20a_t%20&plus;%20b_t%20%5C%5C%20a_t%20%3D%20%5Calpha%20D_t%20&plus;%20%281-%20%5Calpha%29%28F_t%29%20%5C%5C%20b_t%20%3D%20%5Cbeta%20%28a_t-a_t_-_1%29%20&plus;%20%281-%5Cbeta%29b_t_-_1)

- **F** - the forecast at time **t**.
- **D** - the actual value at time **t**.
- **a** - level at time **t**.
- **b** - trend/slope component at time **t**.
- **α** - smoothing parameter for level.
- **β** - smoothing parameter for trend.
  
The following graph illustrates how holt's model is used to forecast time series which have trend component.

![](https://www.vividcortex.com/hubfs/Blog/Double_exponential_smoothing.png)

[Image Source](https://www.vividcortex.com/blog/exponential-smoothing-for-time-series-forecasting)

### Comparison with Linear Regression
- Linear Regression is a effective method used to predict data points, but linear regression considers all data with same weightage.
- This property of LR isn't suitable for time series data, hence holt's is perfered over LR for time series analysis as the model uses the exponential smoothing.


# Author
**Krishnan S G** 
