import os
import pandas as pd
import matplotlib.pyplot as plt
"""
Import a specific range of data from energy_statistical_countrydatasheets.xlsx
"""
def import_countrydatasheet_data(sheet_name, start_row, number_of_rows):
    data = os.path.join(os.path.dirname(__file__), '../data/energy_statistical_countrydatasheets.xlsx')
    df = pd.read_excel(data, sheet_name=sheet_name, index_col=2, usecols="A:AG",
                       skiprows=lambda x: x in range(0, start_row) and x != 7, nrows=number_of_rows, engine='openpyxl')
    df1 = df.drop([8, 'Unnamed: 1'], axis=1)
    return df1, sheet_name

"""
General function for creating stacked bar plots from a table in the scalars-table-format. The input data
must contain only one single country.
"""
# TODO: use country as an input variable
def stacked_scalars_1country(plot_data, title, ylabel, xlabel):
    df_plot = pd.crosstab(index=plot_data.UseCase, columns=plot_data.Parameter, values=plot_data.Value / 1000,
                            aggfunc='mean')

    # TODO: check is_unique, if not issue warning message

    if df_plot.columns.str.contains('Curtailment').any():
        df_plot['EnergyConversion_Curtailment_Electricity_RE'] = df_plot['EnergyConversion_Curtailment_Electricity_RE'] * (-1)
    # Storage should be plotted in a separate diagram. It is therefore herewith allocated to a separate DataFrame
    # and removed from df_plot.
    #    if df_plot.columns.str.contains('Storage').any():
    #        df_storage = df_plot[df_plot.columns.str.contains('Storage')] # doesn't work this way

    df_plot.plot(kind='bar', stacked=True)
    plt.axhline(0, color='black')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/' + title), bbox_inches='tight')