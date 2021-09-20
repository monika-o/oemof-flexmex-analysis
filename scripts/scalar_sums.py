import pandas as pd
import os

def sum_globally(df_in, scenario, co2_price):
    df = df_in.loc[df_in['UseCase']=='FlexMex2_'+scenario]
    df_out = df.groupby(['Parameter']).sum()
    df_out.to_csv(os.path.join(os.path.dirname(__file__), '../results/scalar_sums'+co2_price+scenario+'.csv'))

co2_prices = ['107', '240']

for co2_price in co2_prices:
    input_file = os.path.join(os.path.dirname(__file__), '../../oemof-flexmex/results/FlexMex2_'+co2_price+'/Scalars.csv')

    input = pd.read_csv(input_file)

    sum_globally(input, '2d', co2_price)