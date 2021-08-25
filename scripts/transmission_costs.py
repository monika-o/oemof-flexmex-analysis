import pandas as pd
import os

scalars_ALL_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_ALL.csv')
scalars_ALL = pd.read_csv(scalars_ALL_file)

scalars_ALL = scalars_ALL.loc[scalars_ALL['Parameter'].str.contains('Transmission')]

varom_ALL = scalars_ALL.loc[scalars_ALL.loc[:,'Parameter']=='Transmission_VarOM_Electricity_Grid', 'Value']
varom_ALL = varom_ALL.iloc[0]

length_df = scalars_ALL.loc[scalars_ALL.loc[:,'Parameter']=='Transmission_Length_Electricity_Grid', :]

input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107/Scalars.csv')
input = pd.read_csv(input_file)
input = input.loc[input['Parameter'].str.contains('Transmission_Flows')]

for scenario in ['2a', '2b', '2c', '2d']:
    varom_df = pd.DataFrame()
    data = input.loc[input['UseCase'] == 'FlexMex2_'+scenario]
    for i in range(data.shape[0]):
        region = data.iloc[i, 1]
        if region in length_df['Region'].values:
            length = length_df.loc[length_df['Region']==region, 'Value']
        else:
            chunks = region.split('_')
            region_reversed = chunks[1]+'_'+chunks[0]
            length = length_df.loc[length_df['Region'] == region_reversed, 'Value']

        length = length.iloc[0]
        flow = data.loc[input['Region']==region, 'Value']
        flow = flow.iloc[0]
        row = {'Region': region, 'VarOM': varom_ALL * length * flow / 1000, 'Unit': 'mio Eur'}
        varom_df = varom_df.append(row, ignore_index=True)
    varom_df.to_csv(os.path.join(os.path.dirname(__file__), '../results/107/Transmission_costs_'+scenario+'.csv'))

    total_trans_costs = varom_df['VarOM'].sum()
    print(scenario, total_trans_costs)

    transmission_costs_DE = varom_df.loc[varom_df['Region'].str.contains('_DE'), :]['VarOM'].sum()
    print(scenario, transmission_costs_DE)

    # Annahme: jedes Land hat Kosten für den Import
    # VarOM * transmission length * transmission
    # = Transmission_VarOM_Electricity_Grid [Eur/MWh*km] * Transmission_Length_Electricity_Grid [km] * Transmission_Flows_Electricity_Grid [GWh]