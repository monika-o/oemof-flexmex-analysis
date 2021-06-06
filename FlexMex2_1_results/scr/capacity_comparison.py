import os
import sys
import pandas as pd

input_data_2_1a = os.path.join(os.path.dirname(__file__), '../../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_1a.csv')
df_in = pd.read_csv(input_data_2_1a)

output_2_1a = os.path.join(os.path.dirname(__file__), '../../../oemof-flexmex/results/FlexMex2_1a/03_postprocessed/Scalars.csv')
df_out = pd.read_csv(output_2_1a)

df = pd.DataFrame()
out_values = []


for i in range(len(df_in.loc[:,'Parameter'])):
    for j in range(len(df_out.loc[:, 'Parameter'])):
        if df_in.loc[:, 'Region'][i] == df_out.loc[:, 'Region'][j] and df_in.loc[:, 'Parameter'][i] == df_out.loc[:, 'Parameter'][j]:
            df = df.append([df_in.loc[:,('Region', 'Parameter', 'Value')].iloc[i, :]])
            out_values.append(df_out.loc[:, 'Value'][j])
#                print(df_in.loc[:,('Region', 'Parameter')].iloc[i, :])
        else:
            pass

df['Output_values'] = out_values
df['Out/In'] = out_values / df.loc[:, 'Value']

df.to_csv(os.path.join(os.path.dirname(__file__), '../results/2_1a_comparison.csv'))
print(df)

blathisisachange