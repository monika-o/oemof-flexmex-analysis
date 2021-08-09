import os
import pandas as pd
import matplotlib.pyplot as plt
import analysis.dispatch_plots as plots
from analysis.plot import make_colors_odict

colors_odict = make_colors_odict()

input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_1b/'
                                                     'oemoflex-timeseries/DE-electricity.csv'
                          )
data = pd.read_csv(input_file, header=[0, 1, 2], parse_dates=[0], index_col=[0])

fig, ax = plt.subplots(figsize=(12,5))
ax1 = plt.subplot(2, 1, 1)
data = plots.eng_format(ax1, data, "W", 1000)
start_date='2050-01-01 00:00:00'
end_date='2050-12-01 00:00:00'

plots.plot_dispatch(
    ax1, df=data, bus_name='DE-electricity',
)

datetimeindex = pd.date_range(start="2019-01-01", periods=8760, freq="H")
df = pd.DataFrame()
technologies = ['LiIonBattery']
scenario = '1b'
for technology in technologies:
    # choose 'Heat' or 'Electricity' manually
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_'+scenario+'/Storage/'
                                                     'Electricity/'+technology+'/Level/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
    helper_df = pd.read_csv(input_file)

    df[technology] = helper_df.iloc[:, 1]
    df = df / 1000 # conversion from MWh to GWh
df.set_index(datetimeindex, inplace=True)

ax2 = plt.subplot(2, 1, 2, sharex = ax1)
ax2.plot(df, label = df.columns.values[0], color=colors_odict[technology])
ax2.set_ylabel('Storage level in GWh')
plt.legend()

plt.legend(loc="best")
plt.tight_layout()
plt.show()