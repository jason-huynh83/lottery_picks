from src.logger import logging
from src.exception import CustomException
import datetime
import sys

def data_export(to_send, buy_back):
        logging.info("Data Main is complete")
        logging.info("Entered Data_export phase")
        try:
            today = datetime.datetime.today()
            today_str = today.strftime('%B-%d-%Y')
            
            to_send.to_excel(f"data/April 2023/{today_str}.xlsx")
            print(to_send)
            print('\nbuy back numbers:')
            for row in buy_back['copy_paste']:
                print(row)
        except Exception as e:
            raise CustomException(e, sys)