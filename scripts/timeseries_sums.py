import pandas as pd
import os
import sys

from dispatch_plots import map_labels

scenario = sys.argv[1]

timeseries_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2/'+scenario+
                               '/oemoflex-timeseries/DE-electricity.csv')
df_in = pd.read_csv(timeseries_file, header=[0, 1, 2], index_col=0)

sum = df_in.astype(float).sum()
sum.to_csv(os.path.join(os.path.dirname(__file__), '../results/'
                                                   'sums of timesieries '+scenario + '.csv'))