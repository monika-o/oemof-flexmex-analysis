"""
The aim of this little program is to visualize electricity production, transmission, curtailment and shortage for Germany,
according to the scenarios 2_1a to 2_1d.
The result should be 4 stacked bar charts, one for each scenario.
"""
import sys
import pandas as pd
import os

from analysis.plot import preprocessing_stacked_scalars
from analysis.plot import stacked_scalars
from analysis.preprocessing_scalars import conversion_electricity_FlexMex2_1
from analysis.preprocessing_scalars import conversion_electricity_FlexMex2_2
from analysis.preprocessing_scalars import conversion_heat_FlexMex2_2
from analysis.preprocessing_scalars import storage_FlexMex2_2
from analysis.preprocessing_scalars import storage_FlexMex2_1

scalars_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2/Scalars.csv')
scenario = sys.argv[1] # either FlexMex2_1 or FlexMex2_2
onxaxes = sys.argv[2] # either Region or Scenario

# Retrieve the demand; demand is the same in all scenarios.
# TODO: This is true for demand, but is it also for the other values imported from this scalars file?
demand_file = os.path.join(os.path.dirname(__file__),
                              '../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_2a.csv')

df_demand = pd.read_csv(demand_file)

df_in = pd.read_csv(scalars_file)
df_in.rename(columns = {'UseCase':'Scenario'}, inplace = True)
df_in = df_in[df_in.loc[:,'Scenario'].str.contains(scenario)]
if scenario == 'FlexMex2_1':
    df_plot_conversion_electricity, electricity_demand = conversion_electricity_FlexMex2_1(df_in, df_demand, onxaxes)
    df_plot_storage = storage_FlexMex2_1(df_in, onxaxes)
elif scenario == 'FlexMex2_2':
    df_plot_conversion_electricity, electricity_demand = conversion_electricity_FlexMex2_2(df_in, df_demand, onxaxes)
    df_plot_conversion_heat, heat_demand = conversion_heat_FlexMex2_2(df_in, df_demand, onxaxes)
    df_plot_storage, filler_demand = storage_FlexMex2_2(df_in, onxaxes)

stacked_scalars(df_plot_conversion_electricity, electricity_demand, '2021-07-17-electricity_flows ' + scenario + onxaxes, 'Electricity in GWh', 'Scenario')
stacked_scalars(df_plot=df_plot_storage, demand=0, title='2021-07-17-storage' + scenario + onxaxes,
                    ylabel='storage in GWh', xlabel='Scenario')
if scenario == 'FlexMex2_2':
    stacked_scalars(df_plot_conversion_heat, heat_demand, '2021-07-17-heat_flows ' + scenario + onxaxes, 'Heat in GWh', 'Scenario')
