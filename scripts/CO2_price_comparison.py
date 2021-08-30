"""
Grouped bar plots for changes from elevating the CO2 price
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from analysis.helpers import load_yaml

labels_dict = load_yaml(os.path.join(os.path.dirname(__file__), "../analysis/stacked_plot_labels.yaml"))

def plot_grouped (df, title, ylabel):
    df.sort_index(level=1, inplace=True)
    df.rename(columns=dict(zip(labels_dict.keys(), labels_dict.values())), inplace=True)

    df.dropna(axis=1, inplace=True)
    df = df.loc[:, (df != 0).any(axis=0)]
    df = df.transpose()


    df.plot(
            kind='bar',
            stacked=False,
            title=title,
            figsize=(14, 5)
    )

    plt.ylabel(ylabel)
    plt.tight_layout()

    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/' + title), bbox_inches='tight')


for bus_scenario in ['conv_elec_2_1', 'conv_elec_2_2', 'conv_heat_2_2', 'costs_2_1', 'costs_2_2', 'stor_elec_2_1',
                     'stor_elec_2_2', 'stor_heat_2_2']:

    input_107_21 = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_107_plotted/'
                                                    +bus_scenario+'.csv')

    df_107_21 = pd.read_csv(input_107_21)
    df_107_21.set_index(['Scenario'], inplace=True)


    input_240_21 = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_240_plotted/'
                                                    +bus_scenario+'.csv')


    df_240_21 = pd.read_csv(input_240_21)
    df_240_21.set_index(['Scenario'], inplace=True)

    df_21 = pd.concat([df_107_21, df_240_21], keys=[107.3, 240])
#df.set_index('Scenario', keys)


    plot_grouped(df_21, bus_scenario, '')