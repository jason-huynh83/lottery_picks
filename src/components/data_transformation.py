from src.exception import CustomException
from src.logger import logging
import os
import pandas as pd
import numpy as np


class DataTransformation:
    def __init__(self):
        pass
    
    def text_to_df(self, file_name):

        try:
            nums = []
            bets = []
            with open(file_name, 'r') as file:
                for line in file:
                    all_nums = line.replace('-', ' ').replace('$', ' ').replace('.', ' ').replace(':',' ').replace('=', ' ').replace(',', ' ')
                    nums.append(all_nums.strip().split(' ')[:-1])
                    bets.append(all_nums.strip().split(' ')[-1].strip())

            df1 = pd.DataFrame(nums)
            final_df = pd.concat([df1, pd.Series(bets, name='bet')], axis=1)
            final_df = final_df.replace({None:np.nan}).replace({'':np.nan}).replace({' ':np.nan})
            final_df.loc[1000] = np.nan

            return final_df
        
        except:
            raise CustomException(e, sys)
    