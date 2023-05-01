import streamlit as st
from src.components.data_ingestion import DataIngestion
from src.components.data_run import DataFinal
import streamlit as st
import datetime

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def main():
    today = datetime.datetime.today()
    today_str = today.strftime('%B-%d-%Y')
    st.title(f"Uncle Kevin App: {today_str}")
    
    # Text area for user input
    user_input = st.text_area("Enter lotto bets here:", value='copy & paste here')
    
    data_ingestion_obj = DataIngestion('numbers.txt')
    data = data_ingestion_obj.text_to_df_2(user_input)
    df_final = DataFinal()
    to_send, buy_backs = df_final.data_main(data)

    # Submit button
    if st.button("Submit"):
        # Do something with the user input
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


if __name__ == "__main__":
    main()
