"""
Very simple script to plot any kind of timeseries just as it is. It's written for analysis purposes,
not to demonstrate the results to others.

to be manually adapted: scenario_nr, title, title for 4-weeks-plot; activate or deactivate legend
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import analysis.dispatch_plots as plots
from analysis.plot import plot_timeseries
import datetime

df_out = pd.DataFrame()
df_minmax = pd.DataFrame()
df_in = pd.DataFrame()
parameters_out = ['Charging', 'FeedIn']
battery_levels = ['MaxBatteryLevel', 'MinBatteryLevel']

scenario = '2a'
start_date='2050-02-01 00:00:00'
end_date='2050-03-01 00:00:00'
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