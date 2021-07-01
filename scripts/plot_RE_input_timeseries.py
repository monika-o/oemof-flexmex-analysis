import pandas as pd
import matplotlib.pyplot as plt

from analysis.plot import preprocessing_timeseries
from analysis.plot import plot_timeseries

country = 'DE'
timeseries = ['Wind/Offshore', 'Wind/Onshore', 'Solar/PV']

for i in range(len(timeseries)):
    df_in = preprocessing_timeseries('../../oemof-flexmex/data/In/v0.09/Energy/SecondaryEnergy/' + timeseries[i] +
                                     '/FlexMex2_' + country + '_2050.csv', 'generation')

    title = timeseries[i] + ' time series in ' + country + ', 1 year'
    title = title.replace('/', ' ')
    plot_timeseries(df_in, 'year', country, title, 'hours', 'kW/kW installed capacity')
    title = timeseries[i] + ' time series in ' + country + ', 4 weeks'
    title = title.replace('/', ' ')
    plot_timeseries(df_in, 'weeks', country, title, 'hours', 'kW/kW installed capacity')
