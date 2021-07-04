import os
import pandas as pd
import matplotlib.pyplot as plt
import analysis.dispatch_plots as plots

input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2/FlexMex2_1a/'
                                                     'oemoflex-timeseries/DE-electricity.csv'
                          )
data = pd.read_csv(input_file, header=[0, 1, 2], parse_dates=[0], index_col=[0])

fig, ax = plt.subplots(figsize=(12,5))
data = plots.eng_format(ax, data, "W", 1000)
start_date='2050-05-01 00:00:00'
end_date='2050-06-01 00:00:00'

plots.plot_dispatch(
    ax, df=data, bus_name='A-electricity',
)
plt.legend(loc="best")
plt.tight_layout()
plt.show()