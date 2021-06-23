"""
The aim of this script is to generate a csv file that lists the components of a scenario together with their attributes
in a single csv file.
"""
import sys
import os
import pandas as pd

# first step: read in the scenario file and extract the components from it.
import yaml
from yaml.loader import SafeLoader

input_file_definition = sys.argv[1]
with open(input_file_definition) as f:
    data = yaml.load(f, Loader=SafeLoader)
    components = list(data['components'].keys())
    print(components)

# second step: load all component attribute files for the relevant components.
input_data_list = []
for i in range(len(components)):
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/oemoflex/model_structure/component_attrs/'
                              + components[i] + '.csv')
    input_data = pd.read_csv(input_file)
    input_data = input_data.drop(['type', 'description'], axis = 1)
    input_data = input_data.set_index('attribute')
    input_data['value'] = ''
    for j in range(1, len(input_data.index)):
        input_data.iat[j, 3] = input_data.iloc[j, :].dropna().values[0]
    input_data = input_data.drop(['unit', 'default', 'suffix'], axis = 1)
    input_data_list.append(input_data)
concatenated_df = pd.concat(input_data_list, axis=1)
print(concatenated_df)
concatenated_df.to_csv(sys.argv[2])

# third step: join the data in a pandas dataframe so that no indices a doubled but all occuring indices are there.