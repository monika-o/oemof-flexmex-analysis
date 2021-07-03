import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

colors = {'Solar_PV': '#bcbd22', 'Solar PV': '#bcbd22',
          'Wind': '#407294', 'Wind_Offshore': '#1f77b4', 'Wind Offshore': '#1f77b4',
          'Wind_Onshore': '#00ced1', 'Wind Onshore': '#00ced1',
          'SecondaryEnergy_Electricity_RE': '#069943',
          'SecondaryEnergy_Electricity_Slack': '#bf3636',
          'SecondaryEnergy_Heat_Slack': '#bf3636',
          'SecondaryEnergy_Heat_ElectricityHeat_Large': '#3078a3',
          'Capacity_Heat_ElectricityHeat_Large': '#3078a3',
          'Capacity_Heat_ElectricityHeat_Small': '#6fbeee',
          'SecondaryEnergy_Heat_ElectricityHeat_Small': '#6fbeee',
          'SecondaryEnergy_Heat_Electricity_Large': '#36b07b',
          'Capacity_Heat_Electricity_Large': '#36b07b',
          'Losses_Electricity_Hydro_Reservoir': '#0d1692',
          'EnergyConversion_SecondaryEnergy_Electricity_Hydro_ReservoirPump': '#379484', #blauer machen
          'SecondaryEnergy_Electricity_Hydro_ReservoirPump': '#379484', #blauer machen
          'EnergyConversion_SecondaryEnergy_Electricity_Hydro_ReservoirTurbine': '#65ead3', #blauer machen
          'SecondaryEnergy_Electricity_Hydro_ReservoirTurbine': '#65ead3', #blauer machen
          'EnergyConversion_VarOM_Electricity_Hydro_Reservoir': '', #blauer machen
          'Hydro': '#bfd1ce', #blauer machen
          'H2CavernStorage': '#54f2ff',
          'Storage_Losses_H2_H2CavernStorage': '#3a979f',
          'Storage_Output_H2_H2CavernStorage': '#4350ff',
          'Storage_Input_H2_H2CavernStorage': '#8e93dd',
          'Biomass': '#2ca02c', 'CH4': '#d62728', 'CH4 GT': '#d62728',
          'Capacity_Heat_CH4_Large': '#d46566',
          'SecondaryEnergy_Electricity_CH4_GT': '#d62728', 'CH4_GT': '#d62728',
          'SecondaryEnergy_Heat_Gas_Large': '#b07911',
          'SecondaryEnergy_Electricity_ElectricityHeat_CH4_ExCCGT': '#a81bc3',
          'SecondaryEnergy_Heat_ElectricityHeat_CH4_ExCCGT': '#ca71db',
          'Capacity_ElectricityHeat_CH4_ExCCGT': '#e0a2ec',
          'Capacity ElectricityHeat CH4 ExCCGT': '#e0a2ec',
          'Nuclear': '#e4f200',
          'Combustible Fuels': '#d62728',
          'BAT discharge': '#9467bd',
          'BAT charge': '#e377c2',
          'Import': '#17becf',
          'Shortage': '#ff7f0e',
          'Export': '#8c564b',
          'Curtailment': '#7f7f7f', 'Curtailment_Electricity_RE': '#7f7f7f',
          'Demand': '#000000',
          'Solar Thermal': '#ecd70e',
          'Geothermal': '#cdb79e',
          'Tide, Wave and Ocean': '#133337',
          'Other Sources': '#e0d6ce',
          'LiIonBatteryCharge': '#ff80ed',
          'LiIonBatteryDischarge': '#ffc0cb',
          'Storage_Capacity_Electricity_LiIonBatteryStorage': '#cdb79e',
          'LiIonBatteryStorage': '#cdb79e',
          'Storage_Input_Electricity_LiIonBatteryStorage': '#a4a1e3',
          'Storage_Losses_Electricity_LiIonBatteryStorage': '#694872',
          'Storage_Output_Electricity_LiIonBatteryStorage': '#c321ee',
          'Storage_Capacity_Heat_LargeStorage': '#ce2863',
          'Storage_Capacity_Heat_SmallStorage': '#dd8ca8',
          'Storage_Input_Heat_SmallStorage': '#e5ca8a',
          'Storage_Input_Heat_LargeStorage': '#c321ee',
          'Storage_Losses_Heat_SmallStorage': '#a39269',
          'Storage_Losses_Heat_LargeStorage': '#858052',
          'Storage_Output_Heat_SmallStorage': '#e5a305',
          'Storage_Output_Heat_LargeStorage': '#f4df0b',
          'Storage_Capacity_Electricity_H2CavernStorage': '#1bbf9a',
          'Energy_FinalEnergy_Electricity': '#000000',
          'Energy_FinalEnergy_Electricity_H2': '#5f7c83',
          'Energy_FinalEnergy_Heat_CHP': '#292585',
          'Energy_FinalEnergy_Heat_HeatPump': '#807be7',
          'Transmission_Flows_Electricity_Grid': '#a9a9a9',
          'Transmission_Losses_Electricity_Grid': '#69679f',
          'Transport_AnnualDemand_Electricity_Cars': '#4740ec',
          'Transport_FeedIn_DrivePower_Electricity': '#a4a1e3'

          }

"""
Import a specific range of data from energy_statistical_countrydatasheets.xlsx
"""
def import_countrydatasheet_data(sheet_name, last_row_to_skip, number_of_rows):
    data = os.path.join(os.path.dirname(__file__), '../data/energy_statistical_countrydatasheets.xlsx')
    df = pd.read_excel(data, sheet_name=sheet_name, index_col=2, usecols="A:AG",
                       skiprows=lambda x: x in range(0, last_row_to_skip) and x != 7, nrows=number_of_rows, engine='openpyxl')
    df1 = df.drop([8, 'Unnamed: 1'], axis=1)
    return df1, sheet_name

"""
Functions for creating stacked bar plots from a table in the scalars-table-format. The input data
must contain only one single country.
"""
# TODO: use country as an input variable
def preprocessing_stacked_scalars(plot_data, factor, onxaxes): # put a factor here that the values should be devided be, e.g. 1 or 1000
    df_plot_conversion_heat = pd.DataFrame()
    df_plot_conversion_electricity = pd.DataFrame()
    df_plot_storage_heat = pd.DataFrame()
    df_plot_storage_electricity = pd.DataFrame()
    df_plot_capacity_heat = pd.DataFrame()
    df_plot_capacity_electricity = pd.DataFrame()

    if plot_data['Parameter'].str.contains('EnergyConversion_Capacity_Electricity').any():
        plot_data['Parameter'] = plot_data['Parameter'].str.replace('EnergyConversion_Capacity_Electricity_', '')
    if plot_data['Parameter'].str.contains('EnergyConversion_').any():
        plot_data['Parameter'] = plot_data['Parameter'].str.replace('EnergyConversion_', '')
    if plot_data['Parameter'].str.contains('Storage').any():
        # store storage in a separate dataframe ...
        df_storage = plot_data.loc[plot_data['Parameter'].str.contains('Storage'), :]
        # df_storage['Parameter'] = df_storage['Parameter'].str.replace('Storage_Capacity_Electricity_', '')
        # Show only output and losses and not inputs; capacities should be plotted separately
        df_storage = df_storage.loc[~df_storage['Parameter'].str.contains('Input|Capacity'), :]
        # ... and remove it from the original one
        plot_data = plot_data[~plot_data['Parameter'].str.contains('Storage')]
        if df_storage['Parameter'].str.contains('Heat').any():
            df_storage_heat = df_storage.loc[df_storage['Parameter'].str.contains('Heat'), :]
            df_plot_storage_heat = pd.crosstab(index=df_storage_heat[onxaxes], columns=df_storage_heat.Parameter,
                                               values=df_storage_heat.Value / factor, aggfunc='mean')

        df_storage_electricity = df_storage[~df_storage['Parameter'].str.contains('Heat')]
        df_plot_storage_electricity = pd.crosstab(index=df_storage_electricity[onxaxes],
                                                      columns=df_storage_electricity.Parameter,
                                                      values=df_storage_electricity.Value / factor, aggfunc='mean')
    # do the same for separating heat and electricity, both for storage and for energy conversion
    # It would be better to use a for loop for this (for dataframe in (plot_data, df_storage): ...
    if plot_data['Parameter'].str.contains('SecondaryEnergy_Heat').any():
        df_conversion_heat = plot_data.loc[plot_data['Parameter'].str.contains('SecondaryEnergy_Heat|Energy_FinalEnergy_Heat'), :]
        df_plot_conversion_heat = pd.crosstab(index=df_conversion_heat[onxaxes], columns=df_conversion_heat.Parameter,
                                              values=df_conversion_heat.Value / factor, aggfunc='mean')
    df_conversion_electricity = plot_data[~plot_data['Parameter'].str.contains('SecondaryEnergy_Heat|Energy_FinalEnergy_Heat')]
    if plot_data['Parameter'].str.contains('Capacity_Heat').any():
        df_capacity_heat = plot_data.loc[plot_data['Parameter'].str.contains('Capacity_Heat')]
        df_plot_capacity_heat = pd.crosstab(index=df_capacity_heat[onxaxes], columns=df_capacity_heat.Parameter,
                                            values=df_capacity_heat.Value / factor, aggfunc='mean')
        df_capacity_electricity = plot_data.loc[~plot_data['Parameter'].str.contains('Capacity_Heat')]
        df_plot_capacity_electricity = pd.crosstab(index=df_capacity_electricity[onxaxes], columns=df_capacity_electricity.Parameter,
                                            values=df_capacity_electricity.Value / factor, aggfunc='mean')

#        df_plot_conversion_heat = pd.crosstab(index=df_conversion_heat.UseCase, columns=df_conversion_heat.Parameter,
#                                       values=df_conversion_heat.Value / factor, aggfunc='mean')
#        df_plot_conversion_electricity = pd.crosstab(index=df_conversion_electricity.UseCase, columns=df_conversion_electricity.Parameter,
#                                       values=df_conversion_electricity.Value / factor, aggfunc='mean')

    df_plot_conversion_electricity = pd.crosstab(index=df_conversion_electricity[onxaxes], columns=df_conversion_electricity.Parameter,
                                           values=df_conversion_electricity.Value / factor, aggfunc='mean')

    #df_plot_conversion_electricity = \
    #    df_plot_conversion_electricity.reindex(columns=['Energy_FinalEnergy_Electricity', 'Energy_FinalEnergy_Electricity_H2',
    #                                                    'Energy_FinalEnergy_H2', 'SecondaryEnergy_Electricity_CH4_GT',
    #                                                    'SecondaryEnergy_Electricity_RE', 'SecondaryEnergy_Electricity_Slack',
    #                                                    'Curtailment_Electricity_RE'])
    # TODO: check is_unique, if not issue warning message

    #if df_plot.columns.str.contains('Curtailment').any():
    #    df_plot['Curtailment_Electricity_RE'] = df_plot['Curtailment_Electricity_RE'] * (-1)
    # Storage should be plotted in a separate diagram. It is therefore herewith allocated to a separate DataFrame
    # and removed from df_plot.

    return df_plot_conversion_heat, df_plot_conversion_electricity, df_plot_storage_heat, df_plot_storage_electricity, \
           df_plot_capacity_electricity, df_plot_capacity_heat

# The above preprocessing function has become too complicated and doesn't work for electricity flows in FlexMex2_2 now.
# This is why I now write explicit functions for all the plot_dataframes I need.
def conversion_electricity_FlexMex2_1(plot_data, onxaxes):
    if onxaxes == 'Region':
        plot_data = plot_data.loc[plot_data['Scenario'] == 'FlexMex2_1a', :]
    elif onxaxes == 'Scenario':

        plot_data = plot_data.loc[plot_data['Region'].str.contains('DE'), :]
    else:
        print("Only Region or Scenario can be on the x axes.")
    plot_data.to_csv('2021-07-03_plot_data.csv')

    parameters = ['EnergyConversion_SecondaryEnergy_Electricity_CH4_GT',
                  'EnergyConversion_SecondaryEnergy_Electricity_RE',
                  'EnergyConversion_SecondaryEnergy_Electricity_Slack',
                  'EnergyConversion_Curtailment_Electricity_RE',
                  'Transmission_Flows_Electricity_Grid',
                  'Transmission_Losses_Electricity_Grid']
    plot_data = plot_data.loc[plot_data['Parameter'].isin(parameters)]
    # sum all outgoing and all ingoing transmissions for each scenario
    if onxaxes == 'Scenario':
        for i in ('FlexMex2_1a', 'FlexMex2_1b', 'FlexMex2_1c', 'FlexMex2_1d'):

            df_total_outgoing = plot_data[(plot_data.loc[:, 'Parameter'] =='Transmission_Flows_Electricity_Grid') &
                                          (plot_data.loc[:, 'Scenario'] == i) &
                                          (plot_data.loc[:, 'Region'].str.contains('_DE'))]

            total_outgoing = -df_total_outgoing['Value'].sum()
            row_total_outgoing = {'Scenario':i, 'Region':'DE', 'Parameter':'Transmission_Outgoing', 'Unit':'GWh',
                              'Value':total_outgoing}
            df_total_incoming = plot_data[(plot_data.loc[:, 'Parameter'] =='Transmission_Flows_Electricity_Grid') &
                                          (plot_data.loc[:, 'Scenario'] == i) &
                                          (plot_data.loc[:, 'Region'].str.contains('DE_'))]
            total_incoming = df_total_incoming['Value'].sum()
            row_total_ingoing = {'Scenario': i, 'Region': 'DE', 'Parameter': 'Transmission_Incoming', 'Unit': 'GWh',
                                  'Value': total_incoming}
            df_total_losses = plot_data[(plot_data.loc[:, 'Parameter'] =='Transmission_Losses_Electricity_Grid') &
                                          (plot_data.loc[:, 'Scenario'] == i)]
            total_losses = -df_total_losses['Value'].sum()
            row_total_losses = {'Scenario':i, 'Region':'DE', 'Parameter':'Transmission_Losses', 'Unit':'GWh',
                              'Value':total_losses}

            plot_data.drop(df_total_outgoing.index.to_list(), inplace=True)
            plot_data.drop(df_total_incoming.index.to_list(),  inplace=True)
            plot_data.drop(df_total_losses.index.to_list(), inplace=True)
            plot_data = plot_data.append(row_total_outgoing, ignore_index=True)
            plot_data = plot_data.append(row_total_ingoing, ignore_index=True)
            plot_data = plot_data.append(row_total_losses, ignore_index=True)

    df_plot_conversion_electricity = pd.crosstab(index=plot_data[onxaxes], columns=plot_data.Parameter,
                                           values=plot_data.Value, aggfunc='mean')
    print(df_plot_conversion_electricity)


    import pdb

    pdb.set_trace()


def stacked_scalars(df_plot, title, ylabel, xlabel):
    if df_plot.empty:
        pass
    else:
        # Take care that Energy demand is always in the first row. It would have probably been easier to just add the
        # numbers without appending them to the dataframe.
        total_demand = 0
        if df_plot.columns.str.contains('Energy_FinalEnergy').any():
            total_demand = df_plot.iloc[0,:].sum()
            # The demand should be plotted only as a line and not as a stacked bar.
            df_plot = df_plot.drop(df_plot.index[0])
        df_plot.dropna(axis=1, how='all', inplace = True)
        df_plot.plot(kind='bar', stacked=True, color=colors)
        if total_demand > 0:
            plt.hlines(total_demand, plt.xlim()[0], plt.xlim()[1], label='Demand')
        plt.axhline(0, color='black')
        plt.title(title)
        plt.xlabel(xlabel, fontsize = 12)
        plt.ylabel(ylabel, fontsize = 12)
        plt.legend(bbox_to_anchor=(1,1), loc="upper left")
        plt.savefig(os.path.join(os.path.dirname(__file__), '../results/' + title), bbox_inches='tight')

def preprocessing_timeseries (inputdatapath, type):
    input_file = os.path.join(os.path.dirname(__file__),
                              inputdatapath)
    df_in = pd.read_csv(input_file, index_col='timeindex')
    df_in = df_in[type]
    return(df_in)

def plot_timeseries (df_in, timeframe, label, title, xlabel, ylabel):
    fig = plt.figure()
    fig, ax = plt.subplots()
    if timeframe == 'weeks':
        ax.plot(df_in.iloc[0:168 * 4], label=label)
    elif timeframe == 'year':
        # one point for every day
        # ax.plot(df_in.iloc[range(0, 8760, 24)], label=label)
        # daily averages
        ar = np.zeros(shape=365)

        for i in range (0, 365):
            start = i*24
            end = (i+1)*24
            day_mean = df_in.iloc[range(start, end)].mean()
            ar[i] = day_mean
        ax.plot(ar, label = label)
    # in order to show larger tendencies in wind power, here is another kind of plot with weekly averages
    elif timeframe == 'year-rough':
        ar = np.zeros(shape=52)
        for i in range (0, 52):
            start = i*168
            end = (i+1)*168
            week_mean = df_in.iloc[range(start, end)].mean()
            ar[i] = week_mean
        ax.plot(ar, label = label)
    elif timeframe == 'day':
        ax.plot(df_in.iloc[range(6*168, 6*168 + 24)], label=label) # the first day of the sixth week - the choice of the day is arbitrary
    else:
        print('Only day, weeks, year and year-rough are possible timeframes')
    ax.set_title(title)
    ax.set_ylabel(ylabel, fontsize = 12)
    ax.set_xlabel(xlabel, fontsize = 12)
    ax.legend()  # loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)
    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/timeseries/' + title), bbox_inches='tight')
    # TODO: adjust x-axis depending on timeframe (days or months would be good, not hours)