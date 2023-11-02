from src.logger import logging
from src.exception import CustomException
import datetime
import sys
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

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
                   
                # checking for 2.5 win 
                elif len(common) == 2:
                    # convert to float
                    row_values = [float(value) for value in row]
                    # check if bonus number in bets
                    if bs in row_values[:-1]:
                        df.loc[idx, 'win_or_lose'] = 'W (2.5)'
                        
                    elif sum(1 for x in row_values if x == x) == 3:
                        df.loc[idx, 'win_or_lose'] = '2 number Win'
                        
            elif row.count() == 2:
                betting_nums = row.dropna()[:-1].tolist()
                betting_nums = [int(num) for num in betting_nums]
                
                if betting_nums[0] == bs:
                    df.loc[idx, 'win_or_lose'] = 'W'

        if 'win_or_lose' in df.columns:
            return df[(df['win_or_lose'] == 'W') | (df['win_or_lose'] == 'W (2.5)') | (df['win_or_lose'] == '2 number Win')]
            # return df[~df['win_or_lose'].isnull()]
        
        else:
            return 'No winner'
    
    except Exception as e:
        raise CustomException(e, sys)
    

def extract_nums(url):
    
    # Send a GET request to the website and retrieve the HTML content
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the container div that contains the date
    container = soup.find("div", class_='column is-6 lg-date has-text-right')

    numbers = soup.find("div", class_='column is-12 lg-center-flex')

    date = container.text.strip().replace('\n','').split()
    date = ' '.join(date)

    nums = numbers.find_all('li', class_='lg-number')
    nums_list = [] 
    for num in nums:
        nums_list.append(num.text)
        
    winning_nums = nums_list[:-1]
    bs = nums_list[-1]
    
    return date, winning_nums, bs

def scrape_winning_nums(lotto):
    
    logging.info("Scraping Winning Numbers")
    logging.info("Entered scraping winning numbers")
    try:
        md_url = 'https://lotteryguru.com/canada-lottery-results/ca-mega-dice/ca-mega-dice-results-history'
        dg_url = 'https://lotteryguru.com/canada-lottery-results/ca-daily-grand/ca-daily-grand-results-history'
        six_four_url = 'https://lotteryguru.com/canada-lottery-results/ca-lotto-6-49/ca-lotto-6-49-results-history'
        max_url = 'https://lotteryguru.com/canada-lottery-results/ca-lotto-max/ca-lotto-max-results-history'

        if lotto == 'Megadice':
            date, winning_nums, bs = extract_nums(md_url)
        elif lotto == 'Daily Grand':
            date, winning_nums, bs = extract_nums(dg_url)
        elif lotto == 'Lotto 6/49':
            date, winning_nums, bs = extract_nums(six_four_url)
        else:
            date, winning_nums, bs = extract_nums(max_url)
            
        winning_nums = [int(num) for num in winning_nums]
        bs = int(bs)
        
        return date, winning_nums, bs
             

    except Exception as e:
        raise CustomException(e, sys)
    