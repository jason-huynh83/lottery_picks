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

            # to_send, buy_back = data_obj.add_totals(final_df1, df)
            to_send = data_obj.add_totals(final_df1, df)
            # buy_back = buy_back.replace(0,'')
            # buy_back['bets'] = buy_back.iloc[:,:-1].apply(lambda x: '-'.join(x.dropna().astype(str)), axis=1)
            # buy_back['copy_paste'] = buy_back[['bets','bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
            
            # data_export(to_send, buy_back)

            return to_send
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def data_main_2(self, final_df, buy_back_bonus, buy_back_3n):
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

            
            if len(final_df1.columns) > 2:
                to_send, buy_back = data_obj.add_totals_2(final_df1, df, buy_back_bonus, buy_back_3n)
            else:
                to_send, buy_back = data_obj.add_total_bs(final_df1, df, buy_back_bonus)

            buy_back = buy_back.replace(0,'')
            buy_back['bets'] = buy_back.iloc[:,:-1].apply(lambda x: '-'.join(x.dropna().astype(str)), axis=1)
            buy_back['copy_paste'] = buy_back[['bets','bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
            # data_export(to_send, buy_back)

            return to_send, buy_back
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def data_main_3(self, final_df):
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
            
            # to_send, buy_back = data_obj.add_totals_3(final_df1, df)
            if len(final_df1.columns) > 2:
                to_send, buy_back = data_obj.add_totals_3(final_df1, df)
            else:
                to_send, buy_back = data_obj.add_total_bs_3(final_df1, df)
                
            buy_back = buy_back.replace(0,'')
            buy_back = buy_back[pd.to_numeric(buy_back[0], errors='coerce').notna()]
            
            buy_back['bet'] = buy_back['bet'].astype(int)
            
            buy_back['bets'] = buy_back.iloc[:,:-1].apply(lambda x: '-'.join(x.dropna().astype(str)), axis=1)
            buy_back['copy_paste'] = buy_back[['bets','bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
            
            buy_back['bet'] = pd.to_numeric(buy_back['bet'], errors='coerce').astype(int)

            return to_send, buy_back
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def data_main_3_buyback(self, final_df, buy_back_bonus, buy_back_3n):
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

            
            if len(final_df1.columns) > 2:
                to_send, buy_back = data_obj.add_totals_2(final_df1, df, buy_back_bonus, buy_back_3n)
            else:
                to_send, buy_back = data_obj.add_total_bs(final_df1, df, buy_back_bonus)

            buy_back = buy_back.replace(0,'')
            buy_back['bets'] = buy_back.iloc[:,:-1].apply(lambda x: '-'.join(val for val in x.iloc[0:5].dropna().astype(str)), axis=1)
                # x.dropna().astype(str)), axis=1)
            buy_back['copy_paste'] = buy_back[['bets','bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)   
            
            buy_back['copy_paste_actual'] = buy_back[['bets','actual_buying_back']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)   

            return to_send, buy_back
        
        except Exception as e:
            raise CustomException(e, sys)