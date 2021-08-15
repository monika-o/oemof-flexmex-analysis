import os
import pandas as pd
from analysis.plot import plot_date_series as plot

scenario = '2d'
start_date='2050-01-01 00:00:00'
end_date='2050-12-31 00:00:00'

parameter_storage = 'H2Cavern'

df = pd.DataFrame()



input_CCGT = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_'+scenario+'/CHP/'
                                                     'ExCCGT/ElectricityGeneration/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
helper_df = pd.read_csv(input_CCGT)
helper_df = helper_df/1000 # conversion from MW to GW

df['Co-generation turbine'] = helper_df.iloc[:, 1]

input_H2 = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/FlexMex2_'+scenario+
                              '/Storage/Electricity/'+parameter_storage+'/Level/FlexMex2_'+scenario+'_oemof_DE_2050.csv')
helper_df = pd.read_csv(input_H2)
helper_df = helper_df/1000000 #conversion from MWh to TWh

df[parameter_storage] = helper_df.iloc[:, 1]



plot(df, 'Co-generation turbine and H2 cavern storage levels in FlexMex2_'+scenario,
     'GW (turbine) or TWh (cavern)', start_date=start_date, end_date=end_date)