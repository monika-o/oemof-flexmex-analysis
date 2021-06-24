import pandas as pd
import matplotlib.pyplot as plt
import os

from analysis.plot import preprocessing_timeseries

countrycode = ['AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'FR', 'IT', 'LU', 'NL', 'PL']

df_in = preprocessing_timeseries('../../oemof-flexmex/data/In/v0.09/Energy/FinalEnergy/Electricity/'
                                                     'FlexMex2_' + countrycode[4] + '_2050.csv', 'load')
scalars_in = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_2a.csv')
df_scalars_in = pd.read_csv(scalars_in)
df_scalars_in = df_scalars_in[df_scalars_in['Parameter'].map(lambda x: x == ('Energy_FinalEnergy_Electricity'))]

yearly_electricity = df_scalars_in[df_scalars_in['Region']=='DE']['Value']
print(yearly_electricity)

df_in_unnormalised = df_in * yearly_electricity.values

# little verification that the integral (sum) of the time series matches the total yearly demand:
Summe = sum(df_in_unnormalised)
print(Summe)

fig = plt.figure()
fig, ax = plt.subplots()
ax.plot(df_in_unnormalised.iloc[0:156*4], label=countrycode[4])
ax.set_title('Electricity demand in all scenarios')
# TODO: Question: yearly energy or yearly electricity demand?
ax.set_ylabel('hourly electricity demand [GW (el)]')
ax.set_xlabel('hours')
ax.legend()#loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)

plt.savefig(os.path.join(os.path.dirname(__file__), '../results/electricity_demand_timeseries_4weeks.png'), bbox_inches='tight')

fig = plt.figure()
fig, ax = plt.subplots()
ax.plot(df_in_unnormalised.iloc[range(0, 8760, 24)], label=countrycode[4])
ax.set_title('Electricity demand in all scenarios')
ax.set_ylabel('hourly electricity demand [GW (el)]')
ax.set_xlabel('hours')
ax.legend()
plt.savefig(os.path.join(os.path.dirname(__file__), '../results/electricity_demand_timeseries_year_daily.png'), bbox_inches='tight')

# TODO: put months on the x-axis, not hours.