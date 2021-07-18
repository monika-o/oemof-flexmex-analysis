import os
import sys
import pandas as pd

scenario = sys.argv[1]
region = sys.argv[2]

scalars_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2/Scalars.csv')
df_in = pd.read_csv(scalars_file)
df_in.rename(columns = {'UseCase':'Scenario'}, inplace = True)
df_in = df_in[(df_in.loc[:, 'Unit'] == 'Eur') & (df_in.loc[:, 'Scenario'] == scenario) &(df_in.loc[:, 'Region'] == region)]


input_file = os.path.join(os.path.dirname(__file__),
                              '../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_ALL.csv')
df_input = pd.read_csv(input_file)

df_input['Scenario'] = df_input['Scenario'].str.replace('-', '_')
df_input = df_input.loc[df_input['Unit'].str.contains('Eur|percent Inv'), :]


df_in = df_in.append(df_input)

df_in.to_csv(os.path.join(os.path.dirname(__file__), '../results/costs' + scenario + region + 'csv'))