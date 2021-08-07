"""
The aim of this little program is to visualize the installed capacities from FlexMex2_1a up to FlexMex2_1d.
The result should be a simple stacked bar plot with the models on the x-Axis and the capacities on the y axis,
with the capacities being doubled in each scenario. For the sake of simplicity, this is only done fpr Germany.
In a second plot, the capacities from FlexMex2_1b are visualized, also as bar plots, for all countries.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from analysis.preprocessing_scalars import electricity_conversion_capacity_FlexMex2_1
from analysis.plot import stacked_scalars

scenarios1 = ['1a', '1b', '1c', '1d']
scenarios2 = ['2a', '2b', '2c', '2d']

scalars2_1 = pd.DataFrame()
scalars2_2 = pd.DataFrame()

for i in range(len(scenarios1)):
    input_data = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_'+scenarios1[i]+'.csv')
    helper_df = pd.read_csv(input_data)
    scalars2_1 = scalars2_1.append(helper_df)

for i in range(len(scenarios2)):
    input_data = os.path.join(os.path.dirname(__file__),
                              '../../oemof-flexmex/data/In/v0.09/FlexMex2_Scalars_' + scenarios2[i] + '.csv')
    helper_df = pd.read_csv(input_data)
    scalars2_2 = scalars2_2.append(helper_df)

onxaxes = 'Scenario'

scalars2_2.rename(columns={"UseCase": "Scenario"}, inplace=True)

df_plot_el_conv_cap_FlexMex2_1 = electricity_conversion_capacity_FlexMex2_1(scalars2_1, onxaxes)

stacked_scalars(df_plot=df_plot_el_conv_cap_FlexMex2_1, demand=0,
                title='2021-08-07_Installed electricity conversion capacities in Germany in FlexMex2_1' ,
                ylabel='Installed capacities in GW', xlabel='Scenario')


