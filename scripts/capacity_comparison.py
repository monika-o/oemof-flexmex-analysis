"""
This script generates two plots that compare the installed capacities in FlexMex 2-1 and FlexMex 2-2 with the real
capacities from the statistical country datasheet of the EU commission.
"""
import pandas as pd
import os
from analysis.plot import preprocessing_stacked_scalars
from analysis.plot import stacked_scalars
from analysis.plot import import_countrydatasheet_data

region = 'CZ'
scenario = 'FlexMex2_2a' # also change in Input Data file

input_data = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2/Scalars.csv')
df_in = pd.read_csv(input_data)
df_in = df_in.drop(['Modell', 'Year', 'Comment'], axis = 1)
df_in = df_in.loc[df_in['UseCase'] == scenario, :]

df_region = df_in.loc[df_in['Region'] == region, :]
df_region_MW = df_region.loc[df_region['Unit'].str.contains('MW'), :]
conversion_heat, conversion_electricity, storage_heat, storage_electricity, capacity_electricity, capacity_heat =\
    preprocessing_stacked_scalars(df_region_MW, 1, 'Region')

df1, sheet_name = import_countrydatasheet_data(region, 285, 9)
df2 = df1[df1.columns[[29]]]
df2 = df2.transpose()
df2.index = ['EC statistics 2019']

if 'FlexMex2_2' in scenario:
    capacity_electricity.index = [scenario]
    df_conc = pd.concat([capacity_electricity, df2])

elif 'FlexMex2_1' in scenario:
    conversion_electricity.index = [scenario]
    df_conc = pd.concat([conversion_electricity, df2])

df_conc = df_conc / 1000

stacked_scalars(df_plot=df_conc,  demand = 0, title='Comparison of electricity conversion capacities in ' + scenario + ' with reality 2019 in ' + region,
                ylabel='GW', xlabel='')

# TODO: make colors.scv more flexible so and harmonise labels so that e.g. Solar_PV and Solar PV are the same.