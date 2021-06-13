"""
The aim of this little program is to visualize electricity production, transmission, curtailment and shortage for Germany,
according to the scenarios 2_1a to 2_1d.
The result should be 4 stacked bar charts, one for each scenario.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

input_data = os.path.join(os.path.dirname(__file__), '../../../oemof-flexmex/results/FlexMex2/Scalars.csv')
df_in = pd.read_csv(input_data)

# function for checking if all values in a given series are the same:
# I am going to use this to check units.
def is_unique(s):
    a = s.to_numpy() # s.values (pandas<0.24)
    return (a[0] == a).all()

# general function for creating stacked bar plots from a table in the scalars-table-format:
def stacked_scalars_1country(plot_data, title, ylabel, xlabel):
    df_plot = pd.crosstab(index=plot_data.UseCase, columns=plot_data.Parameter, values=plot_data.Value / 1000,
                            aggfunc='mean')

    # TODO: check is_unique, if not issue warning message
    df_plot.plot(kind='bar', stacked=True)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/' + title), bbox_inches='tight')

df_energy = df_in.loc[df_in['Unit'] == 'GWh', :]
print(df_energy)