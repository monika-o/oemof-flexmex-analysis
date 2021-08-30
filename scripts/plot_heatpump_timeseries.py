"""
The purpose of this script is to demonstrate a shift in small heat pump activity when fossil electricity generation gets more
expensive. The goal is a graph for February in FlexMex2_2a in which the daily variation is visible. On the x-axis
shall be dates and on the y-axis generated heat. In addition, the COP should be plotted on a different y-axis.
"""
import os

import pandas
import pandas as pd
import matplotlib.pyplot as plt
from analysis.plot import filter_timeseries

df = pd.DataFrame()
co2_price = ['107', '240']
start_date='2050-02-01 00:00:00'
end_date='2050-03-01 00:00:00'

for price in co2_price:
    generation_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_'+price+'/FlexMex2_2a/'
                                                            'HeatPump/Small/HeatGeneration/'
                                                            'FlexMex2_2a_oemof_DE_2050.csv')
    generation = pandas.read_csv(generation_file, index_col='timeindex')
    df[price] = generation.iloc[:,0]

df = df/1000 # conversion from MW to GW

COP_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/data/In/v0.09/OtherProfiles/COP/'
                                                   'FlexMex2_DE_2050.csv')
COP = pd.read_csv(COP_file, index_col='timeindex')
df['COP'] = COP.iloc[:,0]

df = filter_timeseries(df, start_date, end_date)

fig, ax1 = plt.subplots(figsize=(23,9))
ax1 = plt.subplot()
ax2 = ax1.twinx()
ax2.plot(df.iloc[:, 2], label='COP', color='#d0d0d0')
ax2.set_ylabel('COP [-]', fontsize = 13)
ax2.legend()

ax1.plot(df.iloc[:, 0], label='CO2 price: 107.3 EUR', linewidth=5, color='#ffa700')
ax1.plot(df.iloc[:, 1], label='CO2 price: 240 EUR', color='#4e004b')
ax1.set_ylabel('Heat generation [GW]', fontsize = 13)
ax1.legend()

ax1.set_title('Heat generation by the small heat pump in relation to the COP', fontsize = 15)
plt.savefig(os.path.join(os.path.dirname(__file__), '../results/240/Small_heatpump.png'))
plt.show()