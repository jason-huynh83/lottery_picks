import pandas as pd
import sys
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.utils import data_export

class DataFinal:
    def __init__(self):
        pass
    def data_main(self, final_df):
        logging.info("Data Transformation is complete")
        logging.info("Entered DataFinal - data_main")
        try:
            data_obj = DataTransformation()
            df = pd.DataFrame()
            idx = 0
       
            for index, row in final_df.iterrows():
                if (row == 0).all():
                    test_df = data_obj.total_numbers(final_df.loc[idx:index-1])
                    idx = index+1
                    df = pd.concat([df, test_df])

            index_df = range(1, len(df)+1)
            df.index = [f'text_{i}' for i in index_df]
            final_df1 = final_df[~final_df[0].isnull()]

            to_send, buy_back = data_obj.add_totals(final_df1, df)
            buy_back['bets'] = buy_back.iloc[:,:-1].apply(lambda x: '-'.join(x.dropna().astype(str)), axis=1)
            buy_back['copy_paste'] = buy_back[['bets','bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)

            # data_export(to_send, buy_back)

            return to_send, buy_back
        
        except Exception as e:
            raise CustomException(e, sys)