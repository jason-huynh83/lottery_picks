from src.logger import logging
from src.exception import CustomException
import datetime
import sys
import pandas as pd
import numpy as np

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
        
def check_winning_nums(df, winning_nums, bs):
    logging.info("Checking Winning Numbers")
    logging.info("Entered check_winning_nums phase")
    try:
        df = df.replace(0, np.nan)
        for idx, row in df.iterrows():
            if row.count() > 2:
                betting_nums = row.dropna()[:-1].tolist()
                betting_nums = [int(num) for num in betting_nums]
                
                set1 = set(betting_nums)
                set2 = set(winning_nums)

                common = set1.intersection(set2)
                    
                if len(common) >= 3:
                    df.loc[idx, 'win_or_lose'] = 'W'
                
                elif row.count() == 2:
                    betting_nums = row.dropna()[:-1].tolist()
                    betting_nums = [int(num) for num in betting_nums]

                    if betting_nums[0] == bs:
                        df.loc[idx, 'win_or_lose'] = 'W'

        if 'win_or_lose' in df.columns:
            return df[~df['win_or_lose'].isnull()]
        
        else:
            return 'No winner'
    
    except Exception as e:
        raise CustomException(e, sys)
    

def extract_nums(game):
    
    date = game.iloc[1, 0]
    all_nums = game.iloc[1, 1].split('-')
    winning_nums = all_nums[:-1]
    bs = all_nums[-1]
    
    return date, winning_nums, bs

def scrape_winning_nums(lotto):
    
    logging.info("Scraping Winning Numbers")
    logging.info("Entered scraping winning numbers")
    try:
        md_url = 'https://www.lottostrategies.com/cgi-bin/winning_of_past_month/100/ONM/ON/Ontario-ON-Mega-Dice-lottery-results.html'
        dg_url = 'https://www.lottostrategies.com/cgi-bin/winning_of_past_month/100/206/ON/Ontario-ON-Daily-Grand-lottery-results.html'
        six_four_url = 'https://www.lottostrategies.com/cgi-bin/winning_of_past_month/100/201/ON'
        max_url = 'https://www.lottostrategies.com/cgi-bin/winning_of_past_month/100/203/ON/Ontario-ON-Lotto-Max-lottery-results.html'

        if lotto == 'Megadice':
            md = pd.read_html(md_url)[1]
            date, winning_nums, bs = extract_nums(md)
        elif lotto == 'Daily Grand':
            dg = pd.read_html(dg_url)[1]
            date, winning_nums, bs = extract_nums(dg)
        elif lotto == 'Lotto 6/49':
            six = pd.read_html(six_four_url)[1]
            date, winning_nums, bs = extract_nums(six)
        else:
            max = pd.read_html(max_url)[1]
            date, winning_nums, bs = extract_nums(max)
            
        winning_nums = [int(num) for num in winning_nums]
            
        return date, winning_nums, bs
             

    except Exception as e:
        raise CustomException(e, sys)
    