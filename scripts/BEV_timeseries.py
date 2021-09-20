import os
import pandas as pd
from analysis.plot import make_colors_odict
from analysis.plot import plot_date_series as plot


colors_odict = make_colors_odict()

df_out = pd.DataFrame()
df_minmax = pd.DataFrame()
df_in = pd.DataFrame()
parameters_out = ['Charging', 'FeedIn']
battery_levels = ['MaxBatteryLevel', 'MinBatteryLevel']

electricity_storages = ['LiIonBattery']#, 'H2Cavern']
heat_storages = ['Large', 'Small']

co2_price = '107'
scenario = '2a'
start_date='2050-01-01 00:00:00'
end_date='2050-12-31 00:00:00'
datetimeindex = pd.date_range(start="2050-01-01", periods=8760, freq="H")
for parameter in parameters_out:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_'+co2_price+'/FlexMex2_'+scenario+'/Transport/'
                                                     'BEV/'+parameter+'/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
    helper_df = pd.read_csv(input_file)
    df_out[parameter] = helper_df.iloc[:, 1]
df_out = df_out / 1000

for parameter in battery_levels:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/OtherProfiles/Transport/'
                              +parameter+'/FlexMex2_DE_2050.csv')
    helper_df = pd.read_csv(input_file)

    df_minmax[parameter] = helper_df.iloc[:, 1]

    df_minmax = df_minmax #* 4690574 * 2.2E-05 #GWh
    df_minmax = df_minmax.rename(columns = {
        'MaxBatteryLevel': 'Maximum battery level',
        'MinBatteryLevel': 'Minimum battery level'})

for parameter in ['DrivePower', 'GridArrivalabilityRate']:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/OtherProfiles/Transport/'
                              +parameter+'/FlexMex2_DE_2050.csv')
    helper_df = pd.read_csv(input_file)

    df_in[parameter] = helper_df.iloc[:, 1]
#    df_out[parameter] = helper_df.iloc[:, 1]*1032000
    df_in = df_in.rename(columns = {
        'DrivePower': 'Drive power',
        'GridArrivalabilityRate': 'Grid arrival ability rate'})

for parameter in ['COP']:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/OtherProfiles/'
                              + parameter + '/FlexMex2_DE_2050.csv')
    df_COP = pd.read_csv(input_file, index_col='timeindex')


title_dict = {
    'df_out': "BEV charging and FeedIn in FlexMex2_"+scenario,
    'df_minmax': "Minimum and maximum battery charging levels",
    'df_in': "Drive power and grid arrival ability rate"
}


plot(df_out, title_dict['df_out'], '[GW]', start_date=start_date, end_date=end_date)
#plot(df_in, title_dict['df_in'], '', start_date=start_date, end_date=end_date)
#plot(df_minmax, title_dict['df_minmax'], 'Share of storage capacity', start_date=start_date, end_date=end_date)
#plot(df_COP, "COP of small heatpumps", 'COP [heat output/electricity input]', start_date=start_date, end_date=end_date)