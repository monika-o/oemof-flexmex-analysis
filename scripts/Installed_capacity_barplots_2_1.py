"""
The aim of this little program is to visualize the installed capacities from FlexMex2_1a up to FlexMex2_1d.
The result should be a simple stacked bar plot with the models on the x-Axis and the capacities on the y axis,
with the capacities being doubled in each scenario. For the sake of simplicity, this is only done fpr Germany.
In a second plot, the capacities from FlexMex2_1b are visualized, also as bar plots, for all countries.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from analysis.plot import preprocessing_stacked_scalars_1country
from analysis.plot import stacked_scalars_1country

# Read all relevant data into a pandas dataframe
input_data = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2/Scalars.csv')
df_in = pd.read_csv(input_data)
df_in = df_in.drop(['Modell', 'Year', 'Comment'], axis = 1)
#print(df_in)

df_DE = df_in.loc[df_in['Region']=='DE', :]
df_DE_cap = df_DE.loc[df_DE['Parameter'].str.contains('Capacity')]
#print(df_DE_cap)

# Because capacities for electricity generation are given in MW and capacities for storages in GWh, they need
# to be separated in my diagram. Or is there a better solution?

# Plot the dataframe

df_plot = preprocessing_stacked_scalars_1country(df_DE_cap, 1000)
stacked_scalars_1country(df_plot, 'Installed capacities in the scenarios 2_1' , 'Installed capacities in GW', 'scenario')

# Now: stacked bar plots for country comparison. Goal: There is one stacked bar plot for each country, all within
# the scenario Flexmex2_1a.

# TODO: general function for the following plot, using colors from plot.py

df_1a = df_in.loc[df_in['UseCase'] == 'FlexMex2_1a', :]
df_1a_cap = df_1a.loc[df_1a['Parameter'].str.contains('Capacity'), :]
df_1a_cap = df_1a_cap.dropna()
df_1a_cap = pd.crosstab(index = df_1a_cap.Region, columns = df_1a_cap.Parameter, values = df_1a_cap.Value/1000, aggfunc = 'mean')
df_1a_cap.drop(['Storage_Capacity_Electricity_LiIonBatteryStorage'], axis = 1, inplace = True)
# BEWARE: Unit of LiIon-batteries is GWh, unit of the others MW!!
df_1a_cap.plot(kind = 'bar', stacked = True)
plt.title('Installed capacities in all countries in the scenario FlexMex2_1a')
plt.ylabel('Installed capacity in GW')

# TODO: embellish the legend

plt.savefig(os.path.join(os.path.dirname(__file__), '../results/Installed capacities in all countries in the scenario FlexMex2_1a.png'), bbox_inches='tight')