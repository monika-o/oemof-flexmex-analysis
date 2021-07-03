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

scalars_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2/Scalars.csv')
scenario = sys.argv[1] # either FlexMex2_1 or FlexMex2_2
onxaxes = sys.argv[2] # either Region or Scenario

df_in = pd.read_csv(scalars_file)
df_in.rename(columns = {'UseCase':'Scenario'}, inplace = True)
df_in = df_in[df_in.loc[:,'Scenario'].str.contains(scenario)]
if scenario == 'FlexMex2_1':
    df_plot_conversion_electricity = conversion_electricity_FlexMex2_1(df_in, onxaxes)
elif scenario == 'FlexMex2_2':
    df_plot_conversion_electricity = conversion_electricity_FlexMex2_2(df_in, onxaxes)

# Retrieve the demand; demand is the same in all scenarios.
# TODO: This is true for demand, but is it also for the other values imported from this scalars file?
demand_file = os.path.join(os.path.dirname(__file__),
                              '../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_2a.csv')

df_demand = pd.read_csv(demand_file)

# Remove Electricity_HeatPump, because HetPumps are explicitly modelled.
df_demand = df_demand[~ (df_demand.loc[:, 'Parameter'] == 'Energy_FinalEnergy_Electricity_HeatPump')]
# Remove FinalEnergy_H2, because I only regard Heat and Electricity.
df_demand = df_demand[~ (df_demand.loc[:, 'Parameter'] == 'Energy_FinalEnergy_H2')]
df_demand = df_demand[df_demand.loc[:, 'Parameter'].str.contains('Energy_FinalEnergy|Transport_AnnualDemand_Electricity_Cars')]
# df_in = df_in.append(df_demand)
# df_plot_conversion_electricity = df_plot_conversion_electricity.append(df_demand)

stacked_scalars(df_plot_conversion_electricity, '2021-07-03-electricity_flows_FlexMex2_1c_all_countries', 'electricity in GWh', 'Scenario')