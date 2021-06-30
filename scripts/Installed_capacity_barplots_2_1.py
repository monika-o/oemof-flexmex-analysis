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

# plot with installed capacities in all regions in scenario 2_1a
df_1a = df_in.loc[df_in['UseCase'] == 'FlexMex2_1a', :]
df_1a_cap = df_1a.loc[df_1a['Parameter'].str.contains('Capacity'), :]
df_1a_cap = df_1a_cap.dropna()

df_plot_conversion_heat, df_plot_conversion_electricity, df_plot_storage_heat, df_plot_storage_electricity = \
    preprocessing_stacked_scalars(df_1a_cap, 1000, 'Region')
stacked_scalars(df_plot_conversion_electricity, 'Installed capacities in all countries in scenario 2_1a' , 'Installed capacities in GW', 'Region')

# plot with installed capacities in Germany in all scenarios (right now only electricity conversion, but can easily be extended)
df_DE = df_in.loc[df_in['Region']=='DE', :]
df_DE_cap = df_DE.loc[df_DE['Parameter'].str.contains('Capacity')]
df_DE_MW = df_DE_cap.loc[df_DE['Unit'].str.contains('MW ')]

df_plot_conversion_heat, df_plot_conversion_electricity, df_plot_storage_heat, df_plot_storage_electricity = \
    preprocessing_stacked_scalars(df_DE_cap, 1000, 'UseCase')

stacked_scalars(df_plot_conversion_electricity, 'Installed capacities in the scenarios 2_1' , 'Installed capacities in GW', 'Scenario')