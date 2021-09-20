import os
import pandas as pd
import matplotlib.pyplot as plt
import analysis.dispatch_plots as plots
from analysis.plot import make_colors_odict
from matplotlib import gridspec

colors_odict = make_colors_odict()
datetimeindex = pd.date_range(start="2050-01-01", periods=8760, freq="H")

region = 'DE'
bus_name = 'DE-electricity' #'DE-electricity','DE-electricity-bev-internal_bus', 'DE-heat_decentral', 'DE-heat_central'
scenario = '1a'
CO2_price = '107' #'fixed_large_heat_storage', '240', '107'

input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_'+CO2_price+'/FlexMex2_'+scenario+
                                                     '/oemoflex-timeseries/'+bus_name+'.csv'
                          )
data = pd.read_csv(input_file, header=[0, 1, 2], parse_dates=[0], index_col=[0])

fig, ax = plt.subplots(figsize=(23,13))
gs = gridspec.GridSpec(ncols=1, nrows=3, figure=fig)

ax1 = plt.subplot(gs[0:2, :])
#ax1 = plt.subplot(2, 1, 1)
data = plots.eng_format(ax1, data, "W", 1000000)
data.set_index(datetimeindex, inplace=True)

start_date='2050-02-01 00:00:00'
end_date='2050-03-01 00:00:00'

#start_date='2050-01-01 00:00:00'
#end_date='2050-12-01 00:00:00'

plots.plot_dispatch(
        ax1, df=data, start_date=start_date, end_date=end_date, bus_name=bus_name,
    )

df = pd.DataFrame()

if bus_name == region+'-electricity':
    technologies = ['LiIonBattery', 'H2Cavern']
    bus = 'Electricity/'
if bus_name == region+'-heat_central':
    technologies = ['Large']
    bus = 'Heat/'
if bus_name == region+'-heat_decentral':
    technologies = ['Small']
    bus = 'Heat/'
if bus_name == region+'-electricity-bev-internal_bus':
    technologies = [] # does not work

for technology in technologies:
    # choose 'Heat' or 'Electricity' manually
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_'+CO2_price+'/FlexMex2_'+scenario+'/Storage/'
                                                     +bus+technology+'/Level/FlexMex2_'+scenario+'_oemof_'+region+'_2050.csv')
    helper_df = pd.read_csv(input_file)
    if technology == 'H2Cavern':
        helper_df = helper_df/1000

    df[technology] = helper_df.iloc[:, 1]

df = df.rename(columns = {'LiIonBattery': 'Li-ion battery',
                          'H2 cavern': 'H2 cavern',
                          'Small': 'Decentralised heat storage',
                          'Large': 'Central heat storage'})

#for i in ['ElectricityGeneration', 'HeatGeneration']:
#    input_file = os.path.join(os.path.dirname(__file__),
#                              '../../oemof-flexmex/results/FlexMex2_' + CO2_price + '/FlexMex2_' + scenario + '/CHP/ExCCGT/'
#                              + i + '/FlexMex2_' + scenario + '_oemof_' + region + '_2050.csv')
#    helper_df = pd.read_csv(input_file)
#    df[i] = helper_df.iloc[:, 1]

df = df / 1000 # conversion from MWh to GWh

#df['power to heat ratio'] = df['ElectricityGeneration']/df['HeatGeneration'] * 10

df.set_index(datetimeindex, inplace=True)
df = plots.filter_timeseries(df, start_date, end_date)

ax2 = plt.subplot(gs[2, :], sharex=ax1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
#ax2 = plt.subplot(2, 1, 2, sharex=ax1)
for i in df.columns:
    if i == 'H2Cavern':
        ax3 = ax2.twinx()
        ax3.plot(df.index, df[i], label='H2 cavern', linewidth = 3, color=colors_odict[i])
        ax3.set_ylabel("H2 cavern storage level [TWh]", fontsize = 20)
        ax2.set_ylabel("Li-ion bat. storage level [GWh]", fontsize = 20)
        ax3.legend(loc=0, fontsize = 20)
        ax2.legend(['Li-ion battery'], loc=2, fontsize = 20)
    else:
        ax2.plot(df.index, df[i], linewidth = 3, color=colors_odict[i])
#plt.set_color(colors_odict)
        ax2.set_ylabel('Storage level [GWh]', fontsize = 20)

        plt.legend(df.columns, loc="best", fontsize = 20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
if CO2_price == '107':
    plt.savefig(os.path.join(os.path.dirname(__file__),'../results/107/Dispatch_'+bus_name+scenario+'.png'))
#if CO2_price == '240':
#    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/240/Dispatch_' + bus_name + scenario + '.png'))
#if CO2_price == 'fixed_large_heat_storage':
#    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/Fixed_large_heat_storage/Dispatch_' + bus_name + scenario + '.png'))