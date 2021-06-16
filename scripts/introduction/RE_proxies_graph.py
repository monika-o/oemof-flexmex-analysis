

"""
Module containing functions to visualize the share of renewable energies in
different sectors in Europe.
"""

import sys
sys.path.append('/home/monika/Documents/TU/Bachelorarbeit/analysis')
import os
import pandas as pd
import numpy as num
import matplotlib as mp
import matplotlib.pyplot as plt
from analysis.plot import import_countrydatasheet_data

print(sys.path)

# Import gross energy consumption data from the xlsx-spreadsheet.
# TODO: Check wether gross energy consumption or final energy consumption are more interesting and which numbers the European goals refer to.

df1, sheet_name = import_countrydatasheet_data('EU27_2020', 69, 23)


# Create a new dataframe with the non-renewables and the renewables added up in 2 lines. The first (gross inland consumption) and the last 3 rows remain.
# TODO: Convert all values into percentages because European goals are given in percentages.

conventional = (df1.loc["Solid fossil fuels"] + df1.loc["Manufactured gases"] + df1.loc["Peat and peat products"]
                + df1.loc["Oil shale and oil sands"] + df1.loc["Oil and petroleum products"] + df1.loc["Natural gas"] + df1.loc["Nuclear"])
df_s = pd.DataFrame(conventional, columns=['Conventional energy']).T
df_s = df_s.append(df1.loc["Renewables and biofuels"])
#print(df_s)

# Check wether conventional + renewables + Electricity + Heat + Waste, non-renewable = Gross inland consumption

difference = df_s.sum(axis=0) + df1.loc["Electricity"] + df1.loc["Heat"] + df1.loc["Waste, non-renewable"] - df1.loc["Gross inland consumption"]
# print(difference)
# result: the difference is negligible


fig = plt.figure()
fig, ax = plt.subplots()
ax.plot(df_s.loc['Conventional energy'], label='Conventional energy')
ax.plot(df_s.loc['Renewables and biofuels'], label='Renewables and biofuels')
ax.plot(df1.loc["Gross inland consumption"], label='Total consumption')
ax.set_title('Gross consumption of conventional and renewable energies in Europe')
ax.set_ylabel('Gross inland consumption [Mtoe]')
ax.legend()#loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)

plt.savefig(os.path.join(os.path.dirname(__file__), '../../results/' + 'RE_development_' + sheet_name +'.png'), bbox_inches='tight')

