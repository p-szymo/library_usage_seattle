# standard dataframe packages
import pandas as pd
import numpy as np

# graphing packages
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style('ticks')

# time-related packages
from statsmodels.tsa.seasonal import seasonal_decompose


def ts_decompose(target):

    '''
    Function to produce a prettified plot of the seasonal decomposition of data.

    Input
    -----
    target : Pandas Series
        Input data.


    Output
    ------
    fig : matplotlib.figure.Figure
        Resultant plot (also printed).

    '''


    # decompose data
    decomposition = seasonal_decompose(target)

    # separate decomposition into parts
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residuals = decomposition.resid
    
    # capture date objects
    start_month = target.index[0].strftime('%B')
    start_day = target.index[0].strftime('%d')
    start_year = target.index[0].strftime('%Y')
    end_month = target.index[-1].strftime('%B')
    end_day = target.index[-1].strftime('%d')
    end_year = target.index[-1].strftime('%Y')

    # instantiate figure
    fig = plt.figure(figsize=(24,16))
    plt.suptitle(f'Decomposition of data ({start_month} {start_day}, {start_year} - {end_month} {end_day}, {end_year})',
                 fontsize=30, y=1.04)

    # plot original data
    plt.subplot(411)
    plt.plot(target, label='Original', color='blue')
    plt.legend(loc='upper left', fontsize=20)
    plt.ylabel('Number of checkouts', fontsize=20, labelpad=15)
    plt.yticks(fontsize=18)
    plt.xlabel('')
    plt.xticks(fontsize=18, rotation=0)

    # plot trend
    plt.subplot(412)
    plt.plot(trend, label='Trend', color='green')
    plt.legend(loc='upper left', fontsize=20)
    plt.ylabel('Number of checkouts', fontsize=20, labelpad=15)
    plt.yticks(fontsize=18)
    plt.xlabel('')
    plt.xticks(fontsize=18, rotation=0)

    # plot seasonality
    plt.subplot(413)
    plt.plot(seasonal,label='Seasonal',color='orange')
    plt.legend(loc='upper left', fontsize=20)
    plt.ylabel('Number of checkouts', fontsize=20, labelpad=15)
    plt.yticks(fontsize=18)
    plt.xlabel('')
    plt.xticks(fontsize=18, rotation=0)

    # plot residuals
    plt.subplot(414)
    plt.plot(residuals,label='Residuals',color='red')
    plt.legend(loc='upper left', fontsize=20)
    plt.ylabel('Number of checkouts', fontsize=20, labelpad=15)
    plt.yticks(fontsize=18)
    plt.xlabel('')
    plt.xticks(fontsize=18, rotation=0)

    # show plot
    plt.tight_layout()
    plt.show()

    return fig


def ts_rolling(target, period='W'):
    
    '''
    Function to produce a prettified plot with time series data, rolling mean, and
    rolling standard deviation.

    Input
    -----
    target : Pandas Series
        Input data.


    Optional input
    --------------
    period : str or int
        Length of time (in days) to calculate rolling statistics.
            Weekly = 'W',
            Monthly = 'M',
            Bi-annually (6 months) = 'B',
            Yearly = 'Y'


    Output
    ------
    fig : matplotlib.figure.Figure
        Resultant plot (also printed).

    '''
    # period is an integer
    if type(period) == int:
        # determine rolling statistics
        roll_mean = target.rolling(window=period, center=False).mean()
        roll_std = target.rolling(window=period, center=False).std()
    
    # period is a string
    else:
        # conversion dictionary
        period_dict = {
            'W': 7,
            'M': 30,
            'B': 180,
            'Y': 365
        }
        # determine rolling statistics
        roll_mean = target.rolling(window=period_dict[period], center=False).mean()
        roll_std = target.rolling(window=period_dict[period], center=False).std()
        
    # plot rolling statistics
    fig = plt.figure(figsize=(20,10))
    plt.plot(target, color='blue', label='Original')
    plt.plot(roll_mean, color='red', label='Rolling Mean')
    plt.plot(roll_std, color='black', label = 'Rolling Std')

    # prettify
    plt.legend(loc='best', fontsize=20)
    plt.title('Rolling Mean & Standard Deviation', fontsize=28, pad=20)
    plt.ylabel('Number of checkouts', fontsize=25, labelpad=15)
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=20)

    plt.show()

    return fig