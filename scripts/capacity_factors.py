import pandas as pd
import matplotlib.pyplot as plt
import os
from analysis.plot import preprocessing_timeseries
from analysis.plot import make_colors_odict

# TODO: merge with plot_RE_input_timeseries
# TODO: import regions from in regions file in oemof-flexmex
colors_odict = make_colors_odict()

region = ['AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'FR', 'IT', 'LU', 'NL', 'PL']
timeseries = ['Wind/Offshore', 'Wind/Onshore', 'Solar/PV']
cap_fact = pd.DataFrame()
for i in range(len(timeseries)):
    for j in range(len(region)):
        df_in = preprocessing_timeseries('../../oemof-flexmex/data/In/v0.09/Energy/SecondaryEnergy/'
                          + timeseries[i] + '/FlexMex2_' + region[j] + '_2050.csv', 'generation')
        cap_fact.loc[timeseries[i], region[j]] = df_in.sum()/8760

fig, ax = plt.subplots(3, 1)
ax1 = plt.subplot(3, 1, 1)
ax2 = plt.subplot(3, 1, 2)
ax3 = plt.subplot(3, 1, 3)
ax1.plot(cap_fact.loc['Solar/PV', :], 'o', color=colors_odict['Solar/PV'])
ax1.set_title('Solar PV')
ax1.set_ylabel('Capacity Factor')
ax2.plot(cap_fact.loc['Wind/Onshore', :], 'o', color=colors_odict['Wind/Onshore'])
ax2.set_title('Wind onshore')
ax2.set_ylabel('Capacity Factor')
ax3.plot(cap_fact.loc['Wind/Offshore', :], 'o', color=colors_odict['Wind/Offshore'])
ax3.set_title('Wind offshore')
ax3.set_ylabel('Capacity Factor')

fig.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__),'../results/capacity_factors.png'))