"""
The aim of this little program is to visualize electricity production, transmission, curtailment and shortage for Germany,
according to the scenarios 2_1a to 2_1d.
The result should be 4 stacked bar charts, one for each scenario.
"""
import sys
import pandas as pd

from analysis.plot import stacked_scalars_1country

# The input file must be a scalars file from oemof-flexmex, e.g. oemof-flexmex/results/FlexMex2/Scalars.csv
# (for models 2_1) or oemof-flexmex/results/FlexMex2_2a/Scalars.csv for the model 2_2a.

input_file_definition = sys.argv[1]
print("What should be the plot's title? e.g. 'Energy flows in Germany for the scenarios FlexMex2_1'")
title = input()
df_in = pd.read_csv(input_file_definition)


df_energy = df_in.loc[df_in['Unit'] == 'GWh', :]
df_energy_DE = df_energy.loc[df_energy['Region'] == 'DE', :]

stacked_scalars_1country(df_energy_DE, title, 'energy in GWh', 'scenario')