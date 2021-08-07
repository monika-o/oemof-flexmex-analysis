import pandas as pd
import os
from analysis.helpers import load_yaml

def generate_labels(df_plot, labels_dict):
    r"""
    Reads in labels for the stacked bar plots for every individual plot

    Parameters
    -------------
    df_plot: pandas.DataFrame
        dataframe to be plotted; column names are the technologies and row names either scenarios or regions.
    labels_dict: pandas.Dictionary (not completely sure about that yet)
        dictionary from stacked_plot_labels.yaml
    Returns
    -------------
    labels: list
        list with labels for one specific plot
    """
    labels = []
    for i in df_plot.columns:
        label = labels_dict[i]
        labels.append(label)
    return labels

dir_name = os.path.abspath(os.path.dirname(__file__))

def onxaxes_preparation(plot_data, onxaxes, scenario_regions):

    if onxaxes == 'Region':
        plot_data = plot_data.loc[plot_data['Scenario'] == scenario_regions, :]
    elif onxaxes == 'Scenario':

        plot_data = plot_data.loc[plot_data['Region'].str.contains('DE'), :] #choose region here
    else:
        print("Only Region or Scenario can be on the x axes.")

    return plot_data


def sum_transmissions(plot_data, scenario,  region):

    df_total_outgoing = plot_data[(plot_data.loc[:, 'Parameter'] == 'Transmission_Flows_Electricity_Grid') &
                                  (plot_data.loc[:, 'Scenario'] == scenario) &
                                  (plot_data.loc[:, 'Region'].str.contains(region + '_'))]

    total_outgoing = -df_total_outgoing['Value'].sum()
    row_total_outgoing = {'Scenario': scenario, 'Region': region, 'Parameter': 'Transmission_Outgoing', 'Unit': 'GWh',
                          'Value': total_outgoing}
    df_total_incoming = plot_data[(plot_data.loc[:, 'Parameter'] == 'Transmission_Flows_Electricity_Grid') &
                                  (plot_data.loc[:, 'Scenario'] == scenario) &
                                  (plot_data.loc[:, 'Region'].str.contains('_' + region))]
    total_incoming = df_total_incoming['Value'].sum()
    row_total_ingoing = {'Scenario': scenario, 'Region': region, 'Parameter': 'Transmission_Incoming', 'Unit': 'GWh',
                         'Value': total_incoming}
    df_total_losses = plot_data[(plot_data.loc[:, 'Parameter'] == 'Transmission_Losses_Electricity_Grid') &
                                (plot_data.loc[:, 'Scenario'] == scenario) &
                                (plot_data.loc[:, 'Region'].str.contains(region))]
    total_losses = -df_total_losses['Value'].sum()
    row_total_losses = {'Scenario': scenario, 'Region': region, 'Parameter': 'Transmission_Losses', 'Unit': 'GWh',
                        'Value': total_losses}

    plot_data.drop(df_total_outgoing.index.to_list(), inplace=True)
    plot_data.drop(df_total_incoming.index.to_list(), inplace=True)
    plot_data.drop(df_total_losses.index.to_list(), inplace=True)
    plot_data = plot_data.append(row_total_outgoing, ignore_index=True) #is substituted by shifted bottom line
    plot_data = plot_data.append(row_total_ingoing, ignore_index=True)
    plot_data = plot_data.append(row_total_losses, ignore_index=True)

    return plot_data

def electricity_conversion_capacity_FlexMex2_1(plot_data, onxaxes):
    plot_data = onxaxes_preparation(plot_data, onxaxes, 'FlexMex2_2c')
    parameters = load_yaml(os.path.join(dir_name, "parameters.yaml"))
    parameters = [*parameters['electricity_conversion_capacity_FlexMex2_1']]
    plot_data = plot_data.loc[plot_data['Parameter'].isin(parameters)]
    df_plot_el_conv_cap_FlexMex2_1 = pd.crosstab(index=plot_data[onxaxes], columns=plot_data.Parameter,
                                                         values=plot_data.Value / 1000, aggfunc='mean')
    return df_plot_el_conv_cap_FlexMex2_1