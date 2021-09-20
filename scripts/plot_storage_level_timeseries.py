"""
Very simple script to plot any kind of time series just as it is. It's written for analysis purposes,
not to demonstrate the results to others.

to be manually adapted: scenario_nr, title, title for 4-weeks-plot; activate or deactivate legend

"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import analysis.dispatch_plots as plots
from analysis.plot import make_colors_odict
from analysis.plot import plot_date_series as plot
from analysis.plot import plot_timeseries
import datetime

colors_odict = make_colors_odict()

electricity_storages = ['LiIonBattery', 'H2Cavern']
heat_storages = ['Large', 'Small']

co2_price = '107'
scenario = '2d'
start_date='2050-01-01 00:00:00'
end_date='2050-12-31 00:00:00'
datetimeindex = pd.date_range(start="2050-01-01", periods=8760, freq="H")


fig, ax = plt.subplots(figsize=(14, 5), linewidth=20)
title = "Storage levels in FlexMex2_"+scenario

ax1 = plt.subplot(2,1,1)
ax3 = plt.subplot(2,1,2, sharex=ax1)

df_electricity = pd.DataFrame()
df_heat = pd.DataFrame()

for parameter in electricity_storages:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_'+co2_price+'/FlexMex2_'+scenario+
                              '/Storage/Electricity/'+parameter+'/Level/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
    helper_df = pd.read_csv(input_file)
    if parameter == 'H2Cavern':
        helper_df = helper_df / 1000
    df_electricity[parameter] = helper_df.iloc[:, 1]

df_electricity = df_electricity / 1000

df_electricity.set_index(datetimeindex, inplace=True)
df_electricity = plots.filter_timeseries(df_electricity, start_date, end_date)
for i in df_electricity.columns:
    if i == 'H2Cavern':
        ax2 = ax1.twinx()
        ax2.set(ylim=(0, 45))
        ax2.plot(df_electricity.index, df_electricity[i], label='H2 cavern', color=colors_odict[i])
        ax2.set_ylabel("H2 cavern [TWh]", fontsize=15)
        ax2.legend(loc=1, fontsize=15)

    else:
        ax1.plot(df_electricity.index, df_electricity[i], linewidth=2, color=colors_odict[i])
        ax1.set(ylim=(0, 458))
ax1.set_ylabel("Battery [GWh]", fontsize=15)
ax1.legend(['Li-ion battery'], loc=2, fontsize=15)


for parameter in heat_storages:
    input_file = os.path.join(os.path.dirname(__file__),
                              '../../oemof-flexmex/results/FlexMex2_'+co2_price+'/FlexMex2_' + scenario +
                              '/Storage/Heat/' + parameter+'/Level/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
    helper_df = pd.read_csv(input_file)
    df_heat[parameter] = helper_df.iloc[:, 1]
df_heat = df_heat / 1000 # from MWh to GWh
df_heat.set_index(datetimeindex, inplace=True)
df_heat = plots.filter_timeseries(df_heat, start_date, end_date)
df_heat.rename(columns={'Large': 'Central heat storage',
                        'Small': 'Decentralised heat storage'}, inplace=True)
for i in df_heat.columns:
    ax3.plot(df_heat.index, df_heat[i], color=colors_odict[i])
ax3.set_ylabel('Heat storage [GWh]', fontsize=15)
ax3.legend(df_heat.columns, fontsize=15)

#plt.title(title)

ax1.tick_params(labelbottom=False)
ax2.tick_params(labelbottom=False)
#plt.show()
plt.savefig(os.path.join(os.path.dirname(__file__), '../results/timeseries/' + title), bbox_inches='tight')