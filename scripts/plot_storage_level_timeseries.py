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

df = pd.DataFrame()
technologies = ['Charging', 'FeedIn']
scenario = '2a'
start_date='2050-02-01 00:00:00'
end_date='2050-03-01 00:00:00'
datetimeindex = pd.date_range(start="2050-01-01", periods=8760, freq="H")
for technology in technologies:
    # choose 'Heat' or 'Electricity' manually
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_'+scenario+'/Transport/'
                                                     'BEV/'+technology+'/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
    helper_df = pd.read_csv(input_file)

    df[technology] = helper_df.iloc[:, 1]
df = df / 1000 # conversion from MWh to GWh
df.set_index(datetimeindex, inplace=True)
df = plots.filter_timeseries(df, start_date, end_date)

# detailed plot over entire year
fig, ax = plt.subplots(figsize=(14,5), linewidth=20)
ax.plot(df)
# plt.legend(df.columns, loc="best") # activate if more than one line is plotted
title = 'BEV charging and FeedIn in FlexMex2_'+scenario
plt.title(title)
#ax.set_xticks([365, 1095, 1825, 2555, 3285, 4015, 4745, 5475, 6205, 6935, 7665, 8395])
#ax.set_xticklabels(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
#                    'October', 'November', 'December'])
plt.ylabel('BEV chargin and FeedIn in GWh', fontsize = 12)
plt.legend(df.columns)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), '../results/timeseries/' + title), bbox_inches='tight')