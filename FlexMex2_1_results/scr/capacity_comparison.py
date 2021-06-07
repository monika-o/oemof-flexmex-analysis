import os
import sys
import pandas as pd

for input_file in ['FlexMex2_Scalars_1a.csv', 'FlexMex2_Scalars_1b.csv', 'FlexMex2_Scalars_1c.csv', 'FlexMex2_Scalars_1d.csv' ]:

    input_data = os.path.join(os.path.dirname(__file__), '../../../oemof-flexmex/data/In/v0.09/' + input_file)
    df_in = pd.read_csv(input_data)

    output = os.path.join(os.path.dirname(__file__), '../../../oemof-flexmex/results/FlexMex2/Scalars.csv')
    df_out = pd.read_csv(output)

    df_out['UseCase'] = df_out['UseCase'].str.replace('_', '-')
    import pdb;

    pdb.set_trace()

    df = pd.DataFrame()
    out_values = []
    scenario = []


    for i in range(len(df_in.loc[:,'Parameter'])):
     for j in range(len(df_out.loc[:, 'Parameter'])):
          if df_in.loc[:, 'Region'][i] == df_out.loc[:, 'Region'][j] and df_in.loc[:, 'Parameter'][i] == df_out.loc[:, 'Parameter'][j]\
                  and df_in.loc[:, 'Scenario'][i] == df_out.loc[:, 'UseCase'][j]:
              df = df.append([df_in.loc[:,('Region', 'Parameter', 'Value')].iloc[i, :]])
              out_values.append(df_out.loc[:, 'Value'][j])
              scenario.append(df_out.loc[:, 'UseCase'][j])
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
