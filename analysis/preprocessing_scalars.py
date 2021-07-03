import pandas as pd

def onxaxes_preparation(plot_data, onxaxes, scenario_regions):
    if onxaxes == 'Region':
        plot_data = plot_data.loc[plot_data['Scenario'] == scenario_regions, :]
    elif onxaxes == 'Scenario':

        plot_data = plot_data.loc[plot_data['Region'].str.contains('DE'), :]
    else:
        print("Only Region or Scenario can be on the x axes.")

    return plot_data

def sum_transmissions(plot_data, scenario,  region):
    df_total_outgoing = plot_data[(plot_data.loc[:, 'Parameter'] == 'Transmission_Flows_Electricity_Grid') &
                                  (plot_data.loc[:, 'Scenario'] == scenario) &
                                  (plot_data.loc[:, 'Region'].str.contains('_'+region))]

    total_outgoing = -df_total_outgoing['Value'].sum()
    row_total_outgoing = {'Scenario': scenario, 'Region': region, 'Parameter': 'Transmission_Outgoing', 'Unit': 'GWh',
                          'Value': total_outgoing}
    df_total_incoming = plot_data[(plot_data.loc[:, 'Parameter'] == 'Transmission_Flows_Electricity_Grid') &
                                  (plot_data.loc[:, 'Scenario'] == scenario) &
                                  (plot_data.loc[:, 'Region'].str.contains(region+'_'))]
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
    plot_data = plot_data.append(row_total_outgoing, ignore_index=True)
    plot_data = plot_data.append(row_total_ingoing, ignore_index=True)
    plot_data = plot_data.append(row_total_losses, ignore_index=True)

    return plot_data

def conversion_electricity_FlexMex2_1(plot_data, onxaxes):
    plot_data = onxaxes_preparation(plot_data, onxaxes, 'FlexMex2_1c')
    plot_data.to_csv('2021-07-03_plot_data.csv')

    parameters = ['EnergyConversion_SecondaryEnergy_Electricity_CH4_GT',
                  'EnergyConversion_SecondaryEnergy_Electricity_RE',
                  'EnergyConversion_SecondaryEnergy_Electricity_Slack',
                  'Transmission_Flows_Electricity_Grid',
                  'Transmission_Losses_Electricity_Grid',
                  'EnergyConversion_Curtailment_Electricity_RE']
    plot_data = plot_data.loc[plot_data['Parameter'].isin(parameters)]
    # sum all outgoing and all ingoing transmissions for each scenario
    if onxaxes == 'Scenario':
        for scenario in ('FlexMex2_1a', 'FlexMex2_1b', 'FlexMex2_1c', 'FlexMex2_1d'):
            plot_data = sum_transmissions(plot_data, scenario, 'DE')
    elif onxaxes == 'Region':
        for region in ('AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'FR', 'IT', 'LU', 'NL', 'PL'):
            plot_data = sum_transmissions(plot_data, 'FlexMex2_1c', region)
            import pdb
            pdb.set_trace

    df_plot_conversion_electricity = pd.crosstab(index=plot_data[onxaxes], columns=plot_data.Parameter,
                                           values=plot_data.Value, aggfunc='mean')
    df_plot_conversion_electricity = \
            df_plot_conversion_electricity.reindex(columns=['EnergyConversion_SecondaryEnergy_Electricity_CH4_GT',
                                                            'EnergyConversion_SecondaryEnergy_Electricity_RE',
                                                            'Transmission_Incoming',
                                                            'EnergyConversion_SecondaryEnergy_Electricity_Slack',
                                                            'EnergyConversion_Curtailment_Electricity_RE',
                                                            'Transmission_Losses',
                                                            'Transmission_Outgoing'])
    return df_plot_conversion_electricity

def conversion_electricity_FlexMex2_2(plot_data, onxaxes):
    plot_data = onxaxes_preparation(plot_data, onxaxes, 'FlexMex2_2c')
    plot_data.to_csv('2021-07-03_plot_data.csv')

    parameters = ['EnergyConversion_SecondaryEnergy_Electricity_CH4_GT',
                  'EnergyConversion_SecondaryEnergy_Electricity_ElectricityHeat_CH4_ExCCGT',
                  'EnergyConversion_SecondaryEnergy_Electricity_RE',
                  'EnergyConversion_SecondaryEnergy_Electricity_Hydro_ReservoirTurbine',
                  'Transport_FeedIn_DrivePower_Electricity',
                  'EnergyConversion_SecondaryEnergy_Electricity_Slack',
                  'EnergyConversion_Curtailment_Electricity_RE',
                  'Transmission_Flows_Electricity_Grid',
                  'Transmission_Losses_Electricity_Grid']
    plot_data = plot_data.loc[plot_data['Parameter'].isin(parameters)]
    # sum all outgoing and all ingoing transmissions for each scenario
    if onxaxes == 'Scenario':
        for scenario in ('FlexMex2_2a', 'FlexMex2_2b', 'FlexMex2_2c', 'FlexMex2_2d'):
            plot_data = sum_transmissions(plot_data, scenario, 'DE')
    elif onxaxes == 'Region':
        for region in ('AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'FR', 'IT', 'LU', 'NL', 'PL'):
            plot_data = sum_transmissions(plot_data, 'FlexMex2_2c', region)

    df_plot_conversion_electricity = pd.crosstab(index=plot_data[onxaxes], columns=plot_data.Parameter,
                                           values=plot_data.Value, aggfunc='mean')
#    df_plot_conversion_electricity = \
#            df_plot_conversion_electricity.reindex(columns=['EnergyConversion_SecondaryEnergy_Electricity_CH4_GT',
#                                                            'EnergyConversion_SecondaryEnergy_Electricity_RE',
#                                                            'Transmission_Incoming',
#                                                            'EnergyConversion_SecondaryEnergy_Electricity_Slack',
#                                                            'EnergyConversion_Curtailment_Electricity_RE',
#                                                            'Transmission_Losses',
#                                                            'Transmission_Outgoing'])
    return df_plot_conversion_electricity

def conversion_heat_FlexMex2_2(plot_data, onxaxes):
    plot_data = onxaxes_preparation(plot_data, onxaxes, 'FlexMex2_2c')
    plot_data.to_csv('2021-07-03_plot_data.csv')

    parameters = ['EnergyConversion_SecondaryEnergy_Heat_Electricity_Large',
                  'EnergyConversion_SecondaryEnergy_Heat_ElectricityHeat_CH4_ExCCGT',
                  'EnergyConversion_SecondaryEnergy_Heat_ElectricityHeat_Large',
                  'EnergyConversion_SecondaryEnergy_Heat_ElectricityHeat_Small',
                  'EnergyConversion_SecondaryEnergy_Heat_Gas_Large',
                  'EnergyConversion_SecondaryEnergy_Heat_Slack',
                  ]
    plot_data = plot_data.loc[plot_data['Parameter'].isin(parameters)]
    # sum all outgoing and all ingoing transmissions for each scenario

    df_plot_conversion_heat = pd.crosstab(index=plot_data[onxaxes], columns=plot_data.Parameter,
                                           values=plot_data.Value, aggfunc='mean')
#    df_plot_conversion_electricity = \
#            df_plot_conversion_electricity.reindex(columns=[])
    return df_plot_conversion_heat