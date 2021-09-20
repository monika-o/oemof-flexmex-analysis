"""
This script generates two plots that compare the installed capacities in FlexMex 2-1 and FlexMex 2-2 with the real
capacities from the statistical country datasheet of the EU commission.
"""
import pandas as pd
import os
import analysis.preprocessing_scalars
import preprocessing_scalars
from analysis.plot import stacked_scalars
from analysis.plot import import_countrydatasheet_data

region = 'DE'
scenario = 'FlexMex2_1a' # also change in Input Data file

input_data = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/Scalars.csv')
df_in = pd.read_csv(input_data)

df_region = df_in.loc[df_in['Region'] == region, :]
df_region.rename(columns={"UseCase": "Scenario"}, inplace=True)

if 'FlexMex2_1' in scenario:
    capacity_electricity = preprocessing_scalars.electricity_conversion_capacity_FlexMex2_1(df_region, 'Scenario')
if 'FlexMex2_2' in scenario:
    capacity_electricity = preprocessing_scalars.electricity_conversion_capacity_FlexMex2_2(df_region, 'Scenario')

df1, sheet_name = import_countrydatasheet_data(region, 285, 9)
df2 = df1[df1.columns[[29]]]
df2 = df2.transpose()
df2 = df2 / 1000
df2.index = ['EC statistics 2019']

df_oemof = capacity_electricity.loc[scenario, :]
df_oemof['Wind'] = df_oemof['EnergyConversion_Capacity_Electricity_Wind_Offshore'] + \
                   df_oemof['EnergyConversion_Capacity_Electricity_Wind_Onshore']
df_oemof = df_oemof.drop(labels = ['EnergyConversion_Capacity_Electricity_Wind_Offshore', 'EnergyConversion_Capacity_Electricity_Wind_Onshore'])


df_oemof = df_oemof.rename({
                 'EnergyConversion_Capacity_Electricity_CH4_GT': 'Gas turbine',
                 'EnergyConversion_Capacity_Electricity_Solar_PV': 'Solar PV'})
if 'FlexMex2_2' in scenario:
    df_oemof.rename({'EnergyConversion_Capacity_ElectricityHeat_CH4_ExCCGT': 'Extraction CHP'})

df2 = df2.append(df_oemof)

if 'FlexMex2_2' in scenario:
    df2 = df2.reindex(columns=['Wind', 'Solar PV', 'Combustible Fuels', 'Gas turbine', 'Extraction CHP', 'Nuclear',
                           'Geothermal', 'Solar Thermal', 'Tide, Wave and Ocean', 'Hydro', 'Other Sources'])
if 'FlexMex2_1' in scenario:
    df2 = df2.reindex(columns=['Wind', 'Solar PV', 'Combustible Fuels', 'Gas turbine', 'Nuclear',
                           'Geothermal', 'Solar Thermal', 'Tide, Wave and Ocean', 'Hydro', 'Other Sources'])
stacked_scalars(df_plot=df2,  demand = 0, title='Comparison of electricity conversion capacities in ' + scenario + ' with reality 2019 in ' + region,
                ylabel='GW', xlabel='')

# TODO: make colors.scv more flexible so and harmonise labels so that e.g. Solar_PV and Solar PV are the same.