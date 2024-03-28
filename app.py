import streamlit as st
from src.components.data_ingestion import DataIngestion
from src.components.data_run import DataFinal
import streamlit as st
from datetime import datetime
from src.utils import check_winning_nums, scrape_winning_nums
import pytz
import math

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def main():
    tz = pytz.timezone('US/Eastern')
    today = datetime.now(tz)
    today_str = today.strftime('%B-%d-%Y')
    st.title(f"Uncle Kevin Lotto App: {today_str}")
    
    # Text area for user input

    user_input = st.text_area("Uncle Kevin Enter lotto bets here:", 
                              placeholder="""Please follow format:
text1
1-2-3$10
4-5-6$50

text2
5-6-7$60
7,6.8$70
                              """,
                              height = 400)

    data_ingestion_obj = DataIngestion('numbers.txt')
    data = data_ingestion_obj.text_to_df(user_input)
        
    # Submit button
    if st.button("Submit"):
        # Do something with the user input
        df_final = DataFinal()
        to_send = df_final.data_main(data)
        st.dataframe(to_send, use_container_width=True)
        csv = convert_df(to_send)
        
        st.download_button(
            label="Download file",
            data=csv,
            file_name=f"{today_str}.csv",
            mime='text/csv',
        )
        # st.write('Buy Back Numbers:')
        # for row in buy_backs['copy_paste']:
        #     st.write(row)

def main_2():
    tz = pytz.timezone('US/Eastern')
    today = datetime.now(tz)
    today_str = today.strftime('%B-%d-%Y')
    
    
    # Text area for user input

    user_input = st.text_area("Jason Enter lotto bets here:", 
                              placeholder="""Please follow format:
text1
1-2-3$10
4-5-6$50

text2
5-6-7$60
7,6.8$70
                              """,
                              height = 400)

    data_ingestion_obj = DataIngestion('numbers.txt')
    data = data_ingestion_obj.text_to_df(user_input)
    
    col1, col2 = st.columns(2)

    # Adding number input widgets in the columns
    with col1:
        buy_back_bonus = st.number_input('Buy Back Bonus', value=100)

    with col2:
        buy_back_3n = st.number_input('Buy Back 3n', value=50)

    # Submit button
    if st.button("Enter"):
    
        df_final = DataFinal()
        to_send, buy_backs = df_final.data_main_2(data, buy_back_bonus, buy_back_3n)
       
        st.dataframe(to_send, use_container_width=True)
        csv = convert_df(to_send)
        
        st.download_button(
            label="Download file",
            data=csv,
            file_name=f"{today_str}.csv",
            mime='text/csv',
        )
        st.write('Buy Back Numbers:')
        for row in buy_backs['copy_paste']:
            st.text(row)

    return data

def main_3():
    tz = pytz.timezone('US/Eastern')
    today = datetime.now(tz)
    today_str = today.strftime('%B-%d-%Y')
    
    
    # Text area for user input

    user_input = st.text_area("Enter lotto bets here:", 
                              placeholder="""Please follow format:
text1
1-2-3$10
4-5-6$50

text2
5-6-7$60
7,6.8$70
                              """,
                              height = 400)

    data_ingestion_obj = DataIngestion('numbers.txt')
    data = data_ingestion_obj.text_to_df(user_input)
    
    buy_back_bonus_toggle, buy_back_3n_toggle = st.columns(2)

    # Adding number input widgets in the columns
    with buy_back_bonus_toggle:
        buy_back_bonus = st.number_input('Buy Back Bonus', value=100, key = 'buy_back_bonus')

    with buy_back_3n_toggle:
        buy_back_3n = st.number_input('Buy Back 3n', value=50, key = 'buy_back_3n')

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    if col1.button("Submit", key="submit_button"):
        df_final = DataFinal()
        to_send, buy_backs = df_final.data_main_3(data)
       
        st.dataframe(to_send, use_container_width=True)
        csv = convert_df(to_send)
        
        st.download_button(
            label="Download file",
            data=csv,
            file_name=f"{today_str}.csv",
            mime='text/csv',
        )
        st.write('Buy Back Numbers:')
        for row in buy_backs['copy_paste']:
            st.text(row)

    # Rearrange button
    if col2.button("Rearrange", key="rearrange_button"):
        
        
        rearr_df = data[data.index != 1000]
        rearr_df[0] = rearr_df[0].astype(int)
        rearr_df['bet'] = rearr_df['bet'].astype(int)
        
        rearr_df = rearr_df.groupby(0)['bet'].sum().reset_index()
        rearr_df = rearr_df.sort_values(by=0, ascending=True)
        
        rearr_df['copy_paste'] = rearr_df[[0,'bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
        
        st.text('bonus')
        for row in rearr_df['copy_paste']:
            st.text(row)
            
    # Rearrange button
    if col3.button("Only Bonus", key="bonus_button"):
        
        bonus_df = data[data.index != 1000]
        bonus_df = bonus_df[bonus_df[1] ==0]
        bonus_df[0] = bonus_df[0].astype(int)
        bonus_df['bet'] = bonus_df['bet'].astype(int)
        
        bonus_df = bonus_df.groupby(0)['bet'].sum().reset_index()
        bonus_df = bonus_df.sort_values(by=0, ascending=True)
        
        bonus_df['copy_paste'] = bonus_df[[0,'bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
        
        st.text('bonus')
        for row in bonus_df['copy_paste']:
            st.text(row)
            
    if col4.button("Only Bonus X2", key='bonus_2x_button'):
        bonus_df = data[data.index != 1000]
        
        if len(bonus_df.columns) > 2:
            bonus_df = bonus_df[bonus_df[1] == 0]
        
        else:
            pass
        
        bonus_df[0] = bonus_df[0].astype(int)
        bonus_df['bet'] = bonus_df['bet'].astype(int)
        
        bonus_df = bonus_df.groupby(0)['bet'].sum().reset_index()
        bonus_df = bonus_df.sort_values(by=0, ascending=True)
        
        # Multiply by 2
        bonus_df['bet'] = bonus_df['bet'] * 2
        
        bonus_df['copy_paste'] = bonus_df[[0,'bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
        
        st.text('bonus')
        for row in bonus_df['copy_paste']:
            st.text(row)
            
    if col5.button("Buy Back", key='buy_back_button'):
        df_final = DataFinal()
        to_send, buy_backs, additional_buy_back = df_final.data_main_3_buyback(data, buy_back_bonus, buy_back_3n)
       
        st.dataframe(to_send, use_container_width=True)
        csv = convert_df(to_send)
        
        st.download_button(
            label="Download file",
            data=csv,
            file_name=f"{today_str}.csv",
            mime='text/csv',
        )
        st.write('Buy Back Numbers:')
        for row in buy_backs['copy_paste']:
            st.text(row)
        
        st.write('Actual Buy Back')
        for row in buy_backs['actual_buyback_copy_paste']:
            st.text(row)
        for row in additional_buy_back['copy_paste']:
            st.text(row)
            
    return data

def winning_numbers():
    lotto_names = ['Megadice','Daily Grand','Lotto 6/49', 'Lotto Max']
    selected_lotto = st.selectbox('Choose Lotto', lotto_names)
    user_input = st.text_area("Enter numbers to check here:", 
                              placeholder="""Please follow format:
text1
1-2-3$10
4-5-6$50

text2
5-6-7$60
7,6.8$70
                              """,
                              height = 400)

    data_ingestion_obj = DataIngestion('numbers.txt')
    data = data_ingestion_obj.text_to_df(user_input)

    # Submit button
    if st.button("Check"):
        date, winning_nums, bs = scrape_winning_nums(selected_lotto)
        st.write(date)
        st.write(', '.join(str(num) for num in winning_nums) + ' bonus ' + str(bs))
        winners = check_winning_nums(data, winning_nums, bs)
        st.write(winners)

if __name__ == "__main__":
    main()
    st.subheader("Check Winning Numbers")
    winning_numbers()
    main_2()
    main_3()