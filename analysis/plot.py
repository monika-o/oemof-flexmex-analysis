import os
import pandas as pd
import matplotlib.pyplot as plt

colors = {'Solar_PV':'#bcbd22', 'Wind': '#407294', 'Wind_Offshore':'#1f77b4', 'Wind_Onshore':'#00ced1', 'Hydro': '#bfd1ce',
          'Biomass':'#2ca02c', 'CH4':'#d62728',
          'CH4_GT': '#d62728', 'Nuclear': '#e4f200',
          'Combustible Fuels': '#d62728', 'BAT discharge': '#9467bd',
          'Import': '#17becf', 'Shortage': '#ff7f0e', 'BAT charge': '#e377c2', 'Export': '#8c564b',
          'Curtailment': '#7f7f7f', 'Curtailment_Electricity_RE': '#7f7f7f', 'Demand': '#000000',
          'Solar Thermal': '#ecd70e', 'Geothermal': '#cdb79e', 'Tide, Wave and Ocean': '#133337',
          'Other Sources': '#e0d6ce',
          'LiIonBatteryCharge': '#ff80ed', 'LiIonBatteryDischarge': '#ffc0cb', 'LiIonBatteryStorage': '#cdb79e',
          'SecondaryEnergy_Electricity_CH4_GT': '#6d562b'}

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
def preprocessing_stacked_scalars_1country(plot_data, factor): # put a factor here that the values should be devided be, e.g. 1 or 1000

    if plot_data['Parameter'].str.contains('EnergyConversion_Capacity_Electricity').any():
        plot_data['Parameter'] = plot_data['Parameter'].str.replace('EnergyConversion_Capacity_Electricity_', '')
    if plot_data['Parameter'].str.contains('EnergyConversion_').any():
        plot_data['Parameter'] = plot_data['Parameter'].str.replace('EnergyConversion_', '')
    if plot_data['Parameter'].str.contains('Storage').any():
        # store storage in a separate dataframe ...
        df_storage = plot_data.loc[plot_data['Parameter'].str.contains('Storage'), :]
#        df_storage['Parameter'] = df_storage['Parameter'].str.replace('Storage_Capacity_Electricity_', '')
        # ... and remove it from the original one
        plot_data = plot_data[~plot_data['Parameter'].str.contains('Storage')]
    # do the same for separating heat and electricity, both for storage and for energy conversion
    # It would be better to use a for loop for this (for dataframe in (plot_data, df_storage): ...
    if plot_data['Parameter'].str.contains('Heat').any():
        df_conversion_heat = plot_data.loc[plot_data['Parameter'].str.contains('Heat'), :]
        df_conversion_electricity = plot_data[~plot_data['Parameter'].str.contains('Heat')]
        import pdb
        pdb.set_trace()
    if df_storage['Parameter'].str.contains('Heat').any():
        df_storage_heat = df_storage.loc[df_storage['Parameter'].str.contains('Heat'), :]
        df_storage_electricity = df_storage[~df_storage['Parameter'].str.contains('Heat')]
# the following code unfortunately didn't work out, so I'm going to skip the for loop and instead copy my code.
#    dataframes = {'df_conversion_heat', 'df_conversion_electricity', 'df_storage_heat', 'df_storage_electricity'}
#    d = {}
#    for i in dataframes:
#        d[i] = pd.crosstab(index=i.UseCase, columns=i.Parameter, values=i.Value / factor,
#                            aggfunc='mean')
    df_plot_conversion_heat = pd.crosstab(index=df_conversion_heat.UseCase, columns=df_conversion_heat.Parameter,
                                       values=df_conversion_heat.Value / factor, aggfunc='mean')
    df_plot_conversion_electricity = pd.crosstab(index=df_conversion_electricity.UseCase, columns=df_conversion_electricity.Parameter,
                                       values=df_conversion_electricity.Value / factor, aggfunc='mean')
    df_plot_storage_heat = pd.crosstab(index=df_storage_heat.UseCase, columns=df_storage_heat.Parameter,
                                       values=df_storage_heat.Value / factor, aggfunc='mean')
    df_plot_storage_electricity = pd.crosstab(index=df_storage_electricity.UseCase, columns=df_storage_electricity.Parameter,
                                       values=df_storage_electricity.Value / factor, aggfunc='mean')


    # TODO: check is_unique, if not issue warning message

    #if df_plot.columns.str.contains('Curtailment').any():
    #    df_plot['Curtailment_Electricity_RE'] = df_plot['Curtailment_Electricity_RE'] * (-1)
    # Storage should be plotted in a separate diagram. It is therefore herewith allocated to a separate DataFrame
    # and removed from df_plot.

    return df_plot_conversion_heat, df_plot_conversion_electricity, df_plot_storage_heat, df_plot_storage_electricity

def stacked_scalars_1country(df_plot, title, ylabel, xlabel):
    df_plot.plot(kind='bar', stacked=True)#, color=colors)
    plt.axhline(0, color='black')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/' + title), bbox_inches='tight')

def preprocessing_timeseries (inputdatapath):
    input_file = os.path.join(os.path.dirname(__file__),
                              inputdatapath)
    df_in = pd.read_csv(input_file, index_col='timeindex')
    df_in = df_in['load']
    return(df_in)