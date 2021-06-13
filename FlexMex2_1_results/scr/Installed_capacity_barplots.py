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

# Read all relevant data into a pandas dataframe
input_data = os.path.join(os.path.dirname(__file__), '../../../oemof-flexmex/results/FlexMex2/Scalars.csv')
df_in = pd.read_csv(input_data)
df_in = df_in.drop(['Modell', 'Year', 'Comment'], axis = 1)
#print(df_in)

df_DE = df_in.loc[df_in['Region']=='DE', :]
df_DE_cap = df_DE.loc[df_DE['Parameter'].str.contains('Capacity')]
#print(df_DE_cap)

# Because capacities for electricity generation are given in MW and capacities for storages in GWh, they need
# to be separated in my diagram. Or is there a better solution?

# Plot the dataframe

fig, ax = plt.subplots()

# A = all EnergyConversion_Capacity_Electricity_CH4_GT for the different models
# B = all EnergyConversion_Capacity_Electricity_Solar_PV for the different models
# C = ... Wind Offshore
# D = ... Wind Onshore
# LiIon Battery must be treated separately

A = np.array(df_DE_cap.loc[df_DE_cap['Parameter'] == 'EnergyConversion_Capacity_Electricity_CH4_GT']['Value'])
B = np.array(df_DE_cap.loc[df_DE_cap['Parameter'] == 'EnergyConversion_Capacity_Electricity_Solar_PV']['Value'])
C = np.array(df_DE_cap.loc[df_DE_cap['Parameter'] == 'EnergyConversion_Capacity_Electricity_Wind_Offshore']['Value'])
D = np.array(df_DE_cap.loc[df_DE_cap['Parameter'] == 'EnergyConversion_Capacity_Electricity_Wind_Onshore']['Value'])

Pos = ('2_1d', '2_1c', '2_1b', '2_1a')
plt.bar(Pos, A, label = 'CH4_GT')
plt.bar(Pos, B, bottom = A, label = 'Solar_PV')
plt.bar(Pos, C, bottom = A + B, label = 'Wind_Offshore')
plt.bar(Pos, D, bottom = A + B + C, label = 'Wind_Onshore')

plt.ylabel('Installed capacity in MW')
plt.xlabel('Scenario')
plt.legend()

plt.show()