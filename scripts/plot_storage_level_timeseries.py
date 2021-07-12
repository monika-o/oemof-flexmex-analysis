"""
Very simple script to plot any kind of timeseries just as it is.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame()
for i in ['d']:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2/FlexMex2_1'+i+'/Storage/'
                                                     'Electricity/LiIonBattery/Level/FlexMex2_1'+i+'_oemof_DE_2050.csv')
    helper_df = pd.read_csv(input_file)

    df[i] = helper_df.iloc[:, 1]
#df.set_index('timeindex')
import pdb
pdb.set_trace()
fig, ax = plt.subplots(figsize=(12,5))
ax.plot(df)
plt.legend(df.columns, loc="best")
plt.tight_layout()
plt.show()