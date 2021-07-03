import pandas as pd

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
    df_plot_conversion_electricity = \
            df_plot_conversion_electricity.reindex(columns=['EnergyConversion_SecondaryEnergy_Electricity_CH4_GT',
                                                            'EnergyConversion_SecondaryEnergy_Electricity_RE',
                                                            'Transmission_Incoming',
                                                            'EnergyConversion_SecondaryEnergy_Electricity_Slack',
                                                            'EnergyConversion_Curtailment_Electricity_RE',
                                                            'Transmission_Losses',
                                                            'Transmission_Outgoing'])
    return df_plot_conversion_electricity

