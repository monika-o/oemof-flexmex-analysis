import os
import pandas as pd

regions = ['AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'FR', 'IT', 'LU', 'NL', 'PL']
co2_price = ['107', '240']

for price in co2_price:
    small_total = 0
    large_total = 0
    for region in regions:
        input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_'+price+'/FlexMex2_2a/'
                                                             'oemoflex-timeseries/'+region+'-electricity.csv')
        input = pd.read_csv(input_file)
        small_df = input.loc[:, input.iloc[0, :] == region+'-electricity-heatpump-small']
        small_sum = small_df.iloc[3:8762, 0].astype(float).sum()
        large_df = input.loc[:, input.iloc[0, :] == region+'-electricity-heatpump-large']
        large_sum = large_df.iloc[3:8762, 0].astype(float).sum()
        print(price, region, small_sum, large_sum)

        small_total += small_sum
        large_total += large_sum
    print('Small total is', small_total)
    print('Large total is', large_total)