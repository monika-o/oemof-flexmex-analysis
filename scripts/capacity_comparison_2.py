"""
This script compared the capacities given in the input data with the capacities given in the results folder.
It was made as support for improving oemof-flexmex.
"""

import os
import pandas as pd

for input_file in ['FlexMex2_Scalars_2a.csv', 'FlexMex2_Scalars_2b.csv', 'FlexMex2_Scalars_2c.csv', 'FlexMex2_Scalars_2d.csv' ]:

    input_data = os.path.join(os.path.dirname(__file__), '../../../oemof-flexmex/data/In/v0.09/' + input_file)
    df_in = pd.read_csv(input_data)

    output = os.path.join(os.path.dirname(__file__), '../../../oemof-flexmex/results/FlexMex2_2a/Scalars.csv')
    df_out = pd.read_csv(output)

    df_out['UseCase'] = df_out['UseCase'].str.replace('_', '-')
    df_out = df_out[df_out['Value'].notna()]
    df_out = df_out[df_out['UseCase'].str.contains('FlexMex2-2')]
    import pdb;

    pdb.set_trace()

    df = pd.DataFrame()
    out_values = []
    scenario = []


    for i in range(len(df_in.loc[:,'Parameter'])):
     for j in range(len(df_out.loc[:, 'Parameter'])):
          if df_in.loc[:, 'Region'].iloc[i] == df_out.loc[:, 'Region'].iloc[j] and df_in.loc[:, 'Parameter'].iloc[i] == df_out.loc[:, 'Parameter'].iloc[j]\
                  and df_in.loc[:, 'Scenario'].iloc[i] == df_out.loc[:, 'UseCase'].iloc[j]:
              df = df.append([df_in.loc[:,('Region', 'Parameter', 'Value')].iloc[i, :]])
              out_values.append(df_out.loc[:, 'Value'].iloc[j])
              scenario.append(df_out.loc[:, 'UseCase'].iloc[j])
          else:
              pass
     print(i, "row of input table compared; total:", len(df_in.loc[:,'Parameter']))
    import pdb;

    pdb.set_trace()
    df['Output_values'] = out_values
    df['Out/In'] = out_values / df.loc[:, 'Value']
    df['Scenario'] = scenario

    df.to_csv(os.path.join(os.path.dirname(__file__), '../results/2_comparison' + input_file))
    print(df)
