import os
import pdb

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from analysis.helpers import load_yaml
from analysis.preprocessing_scalars import generate_labels

dir_name = os.path.abspath(os.path.dirname(__file__))

def make_colors_odict ():
    colors_csv = pd.read_csv(
        os.path.join(dir_name, "colors.csv"), header=[0], index_col=[0])

    colors_csv = colors_csv.T
    colors_odict = OrderedDict()
    for i in colors_csv.columns:
        colors_odict[i] = colors_csv.loc["Color", i]

    return colors_odict

colors_odict = make_colors_odict()

# from analysis import colors


def import_countrydatasheet_data(sheet_name, last_row_to_skip, number_of_rows):

    r"""
    Import a specific range of data from energy_statistical_countrydatasheets.xlsx
    Parameters
    returns
    """
    data = os.path.join(os.path.dirname(__file__), '../data/energy_statistical_countrydatasheets.xlsx')
    df = pd.read_excel(data, sheet_name=sheet_name, index_col=2, usecols="A:AG",
                       skiprows=lambda x: x in range(0, last_row_to_skip) and x != 7, nrows=number_of_rows, engine='openpyxl')
    df1 = df.drop([8, 'Unnamed: 1'], axis=1)
    return df1, sheet_name


def stacked_scalars(df_plot, demand, title, ylabel, xlabel):

    df_plot.dropna(axis=1, how='all', inplace = True)

    labels_dict = load_yaml(os.path.join(dir_name, "stacked_plot_labels.yaml"))

    if df_plot.columns.str.contains('Transmission_Outgoing').any():
        new_df = df_plot.drop('Transmission_Outgoing', axis = 1)
        labels = generate_labels(new_df, labels_dict)
        new_df.plot(kind='bar', stacked=True, bottom = df_plot.loc[:, 'Transmission_Outgoing'], color=colors_odict)
    else:
        labels = generate_labels(df_plot, labels_dict)
        df_plot.plot(kind='bar', stacked=True, color=colors_odict)

    #df_plot = df_plot.drop('Transmission_Outgoing', axis = 1)

    if demand > 0:
        # convert from GWh to TWh
        demand = demand/1000
        plt.hlines(demand, plt.xlim()[0], plt.xlim()[1])#, label='Demand')
        labels.insert(0, 'Demand')
        print(demand)
    plt.axhline(0, color='black', label='_nolegend_')
    plt.title(title)

    plt.xlabel(xlabel, fontsize = 12)
    plt.ylabel(ylabel, fontsize = 12)
    plt.legend(labels, bbox_to_anchor=(1,1), loc="upper left")
    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/' + title), bbox_inches='tight')

def preprocessing_timeseries (inputdatapath, type):
    input_file = os.path.join(os.path.dirname(__file__),
                              inputdatapath)
    df_in = pd.read_csv(input_file, index_col='timeindex')
    df_in = df_in[type]
    return(df_in)

def plot_timeseries (df_in, timeframe, label, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(6,2))
    if timeframe == 'weeks':
        ax.plot(df_in.iloc[0:168 * 4])#, label=label)
    elif timeframe == 'year_hourly':
        ax.plot(df_in)

    elif timeframe == 'year_daily':
        # one point for every day
        # ax.plot(df_in.iloc[range(0, 8760, 24)], label=label)
        # daily averages
        ar = np.zeros(shape=365)

        for i in range (0, 365):
            start = i*24
            end = (i+1)*24
            day_mean = df_in.iloc[range(start, end)].mean()
            ar[i] = day_mean
        ax.plot(ar)#, label = label)
        ax.legend(label)
    # in order to show larger tendencies in wind power, here is another kind of plot with weekly averages
    elif timeframe == 'year_weekly':
        ar = np.zeros(shape=52)
        for i in range (0, 52):
            start = i*168
            end = (i+1)*168
            week_mean = df_in.iloc[range(start, end)].mean()
            ar[i] = week_mean
        ax.plot(ar, label = label)
    elif timeframe == 'day':
        ax.plot(df_in.iloc[range(6*168, 6*168 + 24)], label=label) # the first day of the sixth week - the choice of the day is arbitrary
    else:
        print('Only day, weeks, year and year-rough are possible timeframes')
    ax.set_title(title, fontsize = 15)
    ax.set_ylabel(ylabel, fontsize = 13)
    ax.set_xlabel(xlabel, fontsize = 13)
    #ax.legend(label)  # loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)
    plt.savefig(os.path.join(os.path.dirname(__file__), '../results/timeseries/' + title), bbox_inches='tight')
    # TODO: adjust x-axis depending on timeframe (days or months would be good, not hours)