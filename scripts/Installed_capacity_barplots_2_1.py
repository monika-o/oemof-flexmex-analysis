"""
The aim of this little program is to visualize the installed capacities from FlexMex2_1a up to FlexMex2_1d.
The result should be a simple stacked bar plot with the models on the x-Axis and the capacities on the y axis,
with the capacities being doubled in each scenario. For the sake of simplicity, this is only done fpr Germany.
In a second plot, the capacities from FlexMex2_1b are visualized, also as bar plots, for all countries.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from analysis.plot import preprocessing_stacked_scalars
from analysis.plot import stacked_scalars

# Read all relevant data into a pandas dataframe
input_data = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2/Scalars.csv')
df_in = pd.read_csv(input_data)
df_in = df_in.drop(['Modell', 'Year', 'Comment'], axis = 1)

# capacities in all countries for a specific model
df_1a = df_in.loc[df_in['UseCase'] == 'FlexMex2_2a', :]
df_1a_cap = df_1a.loc[df_1a['Parameter'].str.contains('Capacity'), :]
df_1a_cap = df_1a_cap.dropna()

conversion_heat, conversion_electricity, storage_heat, storage_electricity, capacity_electricity, capacity_heat = \
    preprocessing_stacked_scalars(df_1a_cap, 1000, 'Region')
stacked_scalars(df_plot=capacity_electricity, demand=0, title='2021-07-17_Installed electricity conversion capacities in all countries in FlexMex2_2a' ,
                ylabel='Installed capacities in GW', xlabel='Region')
stacked_scalars(df_plot=capacity_heat, demand=0, title='2021_07_17_Installed heat conversion capacities in all countries in FlexMex2_2a' ,
                ylabel='Installed capacities in GW', xlabel='Region')

# plot with installed capacities in Germany in all scenarios
df_DE = df_in.loc[df_in['Region']=='DE', :]
df_DE = df_DE.loc[df_DE['UseCase'].str.contains('FlexMex2_2'), :]
df_DE_cap = df_DE.loc[df_DE['Parameter'].str.contains('Capacity')]
df_DE_MW = df_DE_cap.loc[df_DE['Unit'].str.contains('MW ')]

conversion_heat, conversion_electricity, storage_heat, storage_electricity, capacity_electricity, capacity_heat = \
    preprocessing_stacked_scalars(df_DE_cap, 1000, 'UseCase')

stacked_scalars(df_plot=capacity_electricity, demand=0, title='2021-07-17_Installed electricity conversion capacities in Germany in FlexMex2_2' ,
                ylabel='Installed capacities in GW', xlabel='Scenario')
stacked_scalars(df_plot=capacity_heat, demand=0, title='2021-07-17_Installed heat conversion capacities in Germany in FlexMex2_2' ,
                ylabel='Installed capacities in GW', xlabel='Scenario')

# plot with storage capacities in Germany - necessary because storage capacities have a different unit
df_DE_storage = df_DE_cap.loc[df_DE_cap['Unit'].str.contains('GWh')]
df_DE_storage = df_DE_storage[df_in.loc[:,'UseCase'].str.contains('FlexMex2_2')]
df_plot_storage_capacities = pd.crosstab(index=df_DE_storage['UseCase'], columns=df_DE_storage.Parameter,
                                               values=df_DE_storage.Value, aggfunc='mean')

stacked_scalars(df_plot=df_plot_storage_capacities, demand=0, title='2021-07-17_Installed storage capacities in FlexMex2_2',
                ylabel='Installed capacities in GWh', xlabel='Scenario')