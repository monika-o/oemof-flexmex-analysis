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

# The input file must be a scalars file from oemof-flexmex, e.g. oemof-flexmex/results/FlexMex2/Scalars.csv
# (for models 2_1) or oemof-flexmex/results/FlexMex2_2a/Scalars.csv for the model 2_2a.


input_file_definition = sys.argv[1]

df_in = pd.read_csv(input_file_definition)
df_in = df_in[df_in.loc[:,'UseCase'].str.contains('FlexMex2_2')]
# Retrieve the demand; demand is the same in all scenarios.
# TODO: This is true for demand, but is it also for the other values imported from this scalars file?
demand_file = os.path.join(os.path.dirname(__file__),
                              '../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_2a.csv')

df_demand = pd.read_csv(demand_file)
df_demand.rename(columns = {'Scenario':'UseCase'}, inplace = True)

# Remove Electricity_HeatPump, because HetPumps are explicitly modelled.
df_demand = df_demand[~ (df_demand.loc[:, 'Parameter'] == 'Energy_FinalEnergy_Electricity_HeatPump')]
# Remove FinalEnergy_H2, because I only regard Heat and Electricity.
df_demand = df_demand[~ (df_demand.loc[:, 'Parameter'] == 'Energy_FinalEnergy_H2')]
df_demand = df_demand[df_demand.loc[:, 'Parameter'].str.contains('Energy_FinalEnergy|Transport_AnnualDemand_Electricity_Cars')]
df_in = df_in.append(df_demand)

# TODO: the two lines below should be input variables to the function
df_energy = df_in.loc[df_in['Unit'].str.contains('GWh|GWh/a'), :]
#df_energy_DE = df_energy.loc[df_energy['Region'] == 'DE', :]

df_energy_DE = df_energy.loc[df_energy['Region'].str.contains('DE'), :]
conversion_heat, conversion_electricity, storage_heat, storage_electricity, capacity_electricity, capacity_heat \
    = preprocessing_stacked_scalars(df_energy_DE, 1, 'UseCase')
#for df in [df_plot_conversion_heat, df_plot_conversion_electricity, df_plot_storage_heat, df_plot_storage_electricity]:
#    print("What should be the plot's title? e.g. 'Energy flows in Germany for FlexMex2_1'. "
#          "The dataframe contains the following parameters ", df.columns)
#    title = input()
#    stacked_scalars(df, title, 'Energy in GWh', 'Scenario')
print("Which scenario is this? FlexMex2_1 or FlexMex2_2?")
scenario = input()
stacked_scalars(conversion_heat, 'Heat flows in Germany in ' + scenario, 'Energy in GWh', 'Scenario')
stacked_scalars(conversion_electricity, 'Electricity flows in Germany in ' + scenario, 'Energy in GWh', 'Scenario')
stacked_scalars(storage_heat, 'Heat flows in Germany in ' + scenario, 'Energy in GWh', 'Scenario')
stacked_scalars(storage_electricity, 'Electricity flows in Germany in ' + scenario, 'Energy in GWh', 'Scenario')
