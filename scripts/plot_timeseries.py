"""
plot electricity demand time series
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

from analysis.plot import preprocessing_timeseries
from analysis.plot import plot_timeseries

# The use of the countrycode list would have only been helpful in a for-loop.
countrycode = ['AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'FR', 'IT', 'LU', 'NL', 'PL']

df_in = preprocessing_timeseries('../../oemof-flexmex/data/In/v0.09/Energy/FinalEnergy/Heat/'
                                                     'FlexMex2_' + countrycode[4] + '_2050.csv', 'load')
scalars_in = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_2a.csv')
df_scalars_in = pd.read_csv(scalars_in)
df_scalars_in = df_scalars_in[df_scalars_in['Parameter'].map(lambda x: x == ('Energy_FinalEnergy_Electricity'))]

yearly_electricity = df_scalars_in[df_scalars_in['Region']=='DE']['Value']
print(yearly_electricity)

#df_in_unnormalised = df_in * yearly_electricity.values
df_in_unnormalised = df_in * 465275


# little verification that the integral (sum) of the time series matches the total yearly demand:
Summe = sum(df_in_unnormalised)
print(Summe)

plot_timeseries(df_in_unnormalised, 'day', countrycode[4], 'Heat demand in all scenarios, 4 weeks', 'hours',
                       'heat demand [GW]')
plot_timeseries(df_in_unnormalised, 'year_daily', countrycode[4], 'Heat demand in all scenarios, 1 year', 'days',
                       'heat demand [GW]')


# TODO: yearly energy or yearly electricity demand? I think electricity, but the timeseries table says energy