import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
from dataclasses import dataclass
import warnings
from src.components.data_run import DataFinal
from io import StringIO
warnings.filterwarnings('ignore')

class DataIngestion:
    def __init__(self, file_name):
        self.file_name = file_name
        
    def text_to_df(self, text_area):
        logging.info("Start of data ingestion")
        try:
            nums = []
            bets = []
            
            text_data = StringIO(text_area)
            df = pd.read_csv(text_data, delimiter="\t", header=None)
            
            for idx, row in df.iterrows():
                all_nums = row[0].replace('-', ' ').replace('$', ' ').replace('.', ' ').replace(':',' ').replace('=', ' ').replace(',', ' ')
                nums.append(all_nums.strip().split(' ')[:-1])
                bets.append(all_nums.strip().split(' ')[-1].strip())

            df1 = pd.DataFrame(nums)
            final_df = pd.concat([df1, pd.Series(bets, name='bet')], axis=1)
            final_df = final_df.replace({None:np.nan}).replace({'':np.nan}).replace({' ':np.nan})
            final_df = final_df.replace({None:0})
            final_df = final_df.drop(0)
            final_df.loc[1000] = 0
            for idx, row in final_df.iterrows():
                if row[0] == 0:
                    final_df.at[idx, 'bet'] = 0

            return final_df
        
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == '__main__':
    obj = DataIngestion('numbers.txt')
    data = obj.text_to_df()
    df_final = DataFinal()
    to_send, buy_backs = df_final.data_main(data)
    logging.info("Proces Complete")

