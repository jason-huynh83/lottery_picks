from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
import sys


class DataTransformation:
    def __init__(self):
        pass

    def add_totals(self, df_running, df):

        logging.info("Entered Data Transformation - adding totals")
        try:
            df_running['bet'] = df_running['bet'].apply(lambda x: int(x))
            buy_backs_3n = df_running[~(df_running[1]==0) & (df_running['bet']>40)]
            buy_backs_bs = df_running[(df_running[1]==0) & (df_running['bet']>80)]

            buy_backs = pd.concat([buy_backs_3n, buy_backs_bs], axis=0)
            buy_backs['bet'] = buy_backs['bet'].apply(lambda x: x-40)
            
            df.loc['Buy Back'] = [-buy_backs[buy_backs[1]==0]['bet'].sum(), -buy_backs[buy_backs[1]!=0]['bet'].sum()]
            bs_total = df['bs'].sum() * 0.13
            n_total = df['3n'].sum() * 0.30
            
            df.loc['Total'] = df.sum()
            df.loc['Total - 13%/30%'] = [df.loc['Total','bs']-bs_total, df.loc['Total','3n']-n_total]
            df.loc['final_total'] = [np.nan, df.loc['Total - 13%/30%', 'bs'] + df.loc['Total - 13%/30%', '3n']]

            return df, buy_backs
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def total_numbers(self, df):
        logging.info("Data Ingestion Complete")
        logging.info("Entered Data Transformation - totaling numbers")
        try:
            df1 = pd.DataFrame()
            df['bet'] = df['bet'].astype(int)
            
            totals_dict = {'bs':df[df[1]==0]['bet'].sum(),
                        '3n':df[df[1]!=0]['bet'].sum()}
            
            totals_df = pd.DataFrame(totals_dict, index=[0])
            
            df_totals = pd.concat([df1, totals_df], ignore_index=True)
            
            return df_totals 
        
        except Exception as e:
            raise CustomException(e, sys)
    