import streamlit as st
from src.components.data_ingestion import DataIngestion
from src.components.data_run import DataFinal
import streamlit as st
from datetime import datetime
from src.utils import check_winning_nums, scrape_winning_nums
import pytz


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
        
    # Submit button
    if st.button("Enter"):
        # Do something with the user input
        df_final = DataFinal()
        to_send, buy_backs = df_final.data_main_2(data)
       
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
            st.write(row)

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