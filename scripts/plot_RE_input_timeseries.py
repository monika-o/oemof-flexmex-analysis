import pandas as pd
import matplotlib.pyplot as plt

from analysis.plot import preprocessing_timeseries
from analysis.plot import plot_timeseries

country = 'DE'
timeseries = ['Wind/Offshore', 'Wind/Onshore', 'Solar/PV', 'Hydro/Reservoir/PowerIn', 'Hydro/Reservoir/PowerOut']

for i in range(len(timeseries)):
    df_in = preprocessing_timeseries('../../oemof-flexmex/data/In/v0.09/Energy/SecondaryEnergy/' + timeseries[i] +
                                     '/FlexMex2_' + country + '_2050.csv', 'generation')

    title = timeseries[i] + ' time series in ' + country + ', 1 year'
    title = title.replace('/', ' ')
    plot_timeseries(df_in, 'year_weekly', country, title, 'weeks', 'kW/kW installed capacity')
    title = timeseries[i] + ' time series in ' + country + ', 4 weeks'
    title = title.replace('/', ' ')
    plot_timeseries(df_in, 'weeks', country, title, 'hours', 'kW/kW installed capacity')
#    title = timeseries[i] + ' time series in ' + country + ', 1 day'
#    title = title.replace('/', ' ')
#    plot_timeseries(df_in, 'day', country, title, 'hours', 'kW/kW installed capacity')

# similar procedure for COP
df_in = preprocessing_timeseries('../../oemof-flexmex/data/In/v0.09/OtherProfiles/COP/FlexMex2_' + country + '_2050.csv',
                                 'load')
title = 'COP for small heatpumps in ' + country
plot_timeseries(df_in, 'year_hourly', country, title, 'hours', 'COP')