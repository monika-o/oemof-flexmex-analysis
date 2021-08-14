import os
import pandas as pd
import matplotlib.pyplot as plt
import analysis.dispatch_plots as plots
from analysis.plot import make_colors_odict
from matplotlib import gridspec

colors_odict = make_colors_odict()
datetimeindex = pd.date_range(start="2050-01-01", periods=8760, freq="H")

bus_name = 'DE-electricity' #'DE-electricity','DE-electricity-bev-internal_bus', 'DE-heat_decentral', 'DE-heat_central'
scenario = '2b' # change also in the input_file path

input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_2b/'
                                                     'oemoflex-timeseries/'+bus_name+'.csv'
                          )
data = pd.read_csv(input_file, header=[0, 1, 2], parse_dates=[0], index_col=[0])

fig, ax = plt.subplots(figsize=(23,9))
gs = gridspec.GridSpec(ncols=1, nrows=3, figure=fig)

ax1 = plt.subplot(gs[0:2, :])
#ax1 = plt.subplot(2, 1, 1)
data = plots.eng_format(ax1, data, "W", 1000)
data.set_index(datetimeindex, inplace=True)

#start_date='2050-02-01 00:00:00'
#end_date='2050-03-01 00:00:00'

start_date='2050-01-01 00:00:00'
end_date='2050-12-01 00:00:00'

plots.plot_dispatch(
        ax1, df=data, start_date=start_date, end_date=end_date, bus_name=bus_name,
    )

df = pd.DataFrame()

if bus_name == 'DE-electricity':
    technologies = ['LiIonBattery', 'H2Cavern']
    bus = 'Electricity/'
if bus_name == 'DE-heat_central':
    technologies = ['Large']
    bus = 'Heat/'
if bus_name == 'DE-heat_decentral':
    technologies = ['Small']
    bus = 'Heat/'


for technology in technologies:
    # choose 'Heat' or 'Electricity' manually
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_'+scenario+'/Storage/'
                                                     +bus+technology+'/Level/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
    helper_df = pd.read_csv(input_file)
    if technology == 'H2Cavern':
        helper_df = helper_df/1000

    df[technology] = helper_df.iloc[:, 1]
df = df / 1000 # conversion from MWh to GWh

df.set_index(datetimeindex, inplace=True)
df = plots.filter_timeseries(df, start_date, end_date)

ax2 = plt.subplot(gs[2, :], sharex=ax1)
#ax2 = plt.subplot(2, 1, 2, sharex=ax1)
for i in df.columns:
    if i == 'H2Cavern':
        ax3 = ax2.twinx()
        ax3.plot(df.index, df[i], label='H2 cavern', color=colors_odict[i])
        ax3.set_ylabel("H2 cavern storage level in TWh")
        ax2.set_ylabel("Li-ion battery storage level in GWh")
        ax3.legend(loc=0)
        ax2.legend(['Li-ion battery'], loc=2)
    else:
        ax2.plot(df.index, df[i], color=colors_odict[i])
#plt.set_color(colors_odict)
        ax2.set_ylabel('Storage level in GWh')

        plt.legend(df.columns, loc="best")


plt.tight_layout()
plt.show()
#plt.savefig(os.path.join(os.path.dirname(__file__),'../results/timeseries/Dispatch'+bus_name+scenario+'.png'))