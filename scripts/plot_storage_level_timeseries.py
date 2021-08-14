"""
Very simple script to plot any kind of timeseries just as it is. It's written for analysis purposes,
not to demonstrate the results to others.

to be manually adapted: scenario_nr, title, title for 4-weeks-plot; activate or deactivate legend
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import analysis.dispatch_plots as plots
from analysis.plot import make_colors_odict
from analysis.plot import plot_timeseries
import datetime

colors_odict = make_colors_odict()

df_out = pd.DataFrame()
df_minmax = pd.DataFrame()
df_in = pd.DataFrame()
parameters_out = ['Charging', 'FeedIn']
battery_levels = ['MaxBatteryLevel', 'MinBatteryLevel']

electricity_storages = ['LiIonBattery', 'H2Cavern']
heat_storages = ['Large', 'Small']

scenario = '2b'
start_date='2050-01-01 00:00:00'
end_date='2050-12-31 00:00:00'
datetimeindex = pd.date_range(start="2050-01-01", periods=8760, freq="H")
for parameter in parameters_out:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_'+scenario+'/Transport/'
                                                     'BEV/'+parameter+'/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
    helper_df = pd.read_csv(input_file)

    df_out[parameter] = helper_df.iloc[:, 1]

for parameter in battery_levels:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/OtherProfiles/Transport/'
                              +parameter+'/FlexMex2_DE_2050.csv')
    helper_df = pd.read_csv(input_file)

    df_minmax[parameter] = helper_df.iloc[:, 1]

    df_minmax = df_minmax #* 4690574 * 2.2E-05 #GWh

for parameter in ['DrivePower', 'GridArrivalabilityRate']:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/OtherProfiles/Transport/'
                              +parameter+'/FlexMex2_DE_2050.csv')
    helper_df = pd.read_csv(input_file)

    df_in[parameter] = helper_df.iloc[:, 1]

for parameter in ['COP']:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/OtherProfiles/'
                              + parameter + '/FlexMex2_DE_2050.csv')
    df_COP = pd.read_csv(input_file, index_col='timeindex')


title_dict = {
    'df_out': "BEV charging and FeedIn in FlexMex2_"+scenario,
    'df_minmax': "Minimum and maximum battery charging levels",
    'df_in': "Drive power and grid arrival ability rate"
}

def plot (df, title, ylabel, start_date = start_date, end_date = end_date):
    df.set_index(datetimeindex, inplace=True)
    df = plots.filter_timeseries(df, start_date, end_date)
    fig, ax = plt.subplots(figsize=(14,5), linewidth=20)
    ax.plot(df)
    title = title
    plt.title(title)
    plt.ylabel(ylabel, fontsize = 12)
    plt.legend(df.columns)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/timeseries/' + title), bbox_inches='tight')

plot(df_out, title_dict['df_out'], 'dont know')
plot(df_in, title_dict['df_in'], 'Share of storage or charging capacity')
plot(df_minmax, title_dict['df_minmax'], 'Share of storage capacity')
plot(df_COP, "COP of small heatpumps", 'COP [heat output/electricity input]')

#####################################################################

fig, ax = plt.subplots(figsize=(14, 5), linewidth=20)
title = "Storage levels in FlexMex2_"+scenario

ax1 = plt.subplot(2,1,1)
ax3 = plt.subplot(2,1,2)

df_electricity = pd.DataFrame()
df_heat = pd.DataFrame()

for parameter in electricity_storages:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_'+scenario+
                              '/Storage/Electricity/'+parameter+'/Level/FlexMex2_'+scenario+'_oemof_BE_2050.csv')
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
        ax2.plot(df_electricity.index, df_electricity[i], label='H2 cavern', color=colors_odict[i])
        ax2.set_ylabel("H2 cavern storage level in TWh")
        ax1.set_ylabel("Li-ion battery storage level in GWh")
        ax2.legend(loc=0)
        ax1.legend(['Li-ion battery'], loc=2)
    else:
        ax1.plot(df_electricity.index, df_electricity[i], color=colors_odict[i])

for parameter in heat_storages:
    input_file = os.path.join(os.path.dirname(__file__),
                              '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_' + scenario +
                              '/Storage/Heat/' + parameter+'/Level/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
    helper_df = pd.read_csv(input_file)
    df_heat[parameter] = helper_df.iloc[:, 1]
df_heat = df_heat / 1000 # from MWh to GWh
df_heat.set_index(datetimeindex, inplace=True)
df_heat = plots.filter_timeseries(df_heat, start_date, end_date)
for i in df_heat.columns:
    ax3.plot(df_heat.index, df_heat[i], color=colors_odict[i])
ax3.set_ylabel('Heat storage levels in GWh')
ax3.legend(df_heat.columns)
plt.title(title)

ax1.tick_params(labelbottom=False)
ax2.tick_params(labelbottom=False)
plt.savefig(os.path.join(os.path.dirname(__file__), '../results/timeseries/' + title), bbox_inches='tight')