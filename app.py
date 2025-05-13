import streamlit as st
from src.components.data_ingestion import DataIngestion
from src.components.data_run import DataFinal
from datetime import datetime
from src.utils import check_winning_nums, scrape_winning_nums
import pytz
import pandas as pd

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

def main_2():
    tz = pytz.timezone('US/Eastern')
    today = datetime.now(tz)
    today_str = today.strftime('%B-%d-%Y')

    st.subheader("🎰 Submit Your Lotto Bets")
    user_input = st.text_area("Jason Enter lotto bets here:", placeholder="""Please follow format:
text1
1-2-3$10
4-5-6$50

text2
5-6-7$60
7,6.8$70
""", height=400)

    data_ingestion_obj = DataIngestion('numbers.txt')
    data = data_ingestion_obj.text_to_df(user_input)

    if 'bb_bonus_perct' not in st.session_state:
        st.session_state.bb_bonus_perct = 0.12
    if 'bb_3n_perct' not in st.session_state:
        st.session_state.bb_3n_perct = 0.25

    button_12, button_25 = st.columns(2)

    with button_12:
        if st.button('12%/25% (Wed, Sat, Sun)'):
            st.session_state.bb_bonus_perct = 0.12
            st.session_state.bb_3n_perct = 0.25

    with button_25:
        if st.button('13%/30% (Mon, Tues, Thurs, Fri)'):
            st.session_state.bb_bonus_perct = 0.13
            st.session_state.bb_3n_perct = 0.30

    col1, col2 = st.columns(2)
    with col1:
        buy_back_bonus = st.number_input('Buy Back Bonus', value=100)
    with col2:
        buy_back_3n = st.number_input('Buy Back 3n', value=50)

    if st.button("✅ Enter"):
        df_final = DataFinal()
        to_send, buy_backs = df_final.data_main_2(data, buy_back_bonus, buy_back_3n, st.session_state.bb_bonus_perct, st.session_state.bb_3n_perct)

        st.dataframe(to_send, use_container_width=True)
        csv = convert_df(to_send)
        st.download_button("📥 Download file", data=csv, file_name=f"{today_str}.csv", mime='text/csv')

        st.write('Buy Back Numbers:')
        for row in buy_backs['copy_paste']:
            if '$' in row and row.split('$')[1]:
                st.text(row)

    col3, col4 = st.columns(2)
    with col3:
        threshold = st.number_input('Buy back threshold', value=50)
    with col4:
        total_bets = st.number_input('Total Bets', value=500)

    if st.button('➗ Calculate'):
        num_lines = int(total_bets / threshold)
        st.text('649')
        for i in range(num_lines):
            st.text(f'1-2-{threshold}')
            total_bets -= threshold
        if total_bets != 0:
            st.text(f'1-2-{total_bets}')

    return data

def main_3():
    tz = pytz.timezone('US/Eastern')
    today = datetime.now(tz)
    today_str = today.strftime('%B-%d-%Y')

    st.subheader("🎰 Submit Your Lotto Bets")
    user_input = st.text_area("Uncle Kevin Enter lotto bets here:", placeholder="""Please follow format:
text1
1-2-3$10
4-5-6$50

text2
5-6-7$60
7,6.8$70
""", height=400)

    data_ingestion_obj = DataIngestion('numbers.txt')
    data = data_ingestion_obj.text_to_df(user_input)

    if st.button("✅ Submit"):
        df_final = DataFinal()
        to_send = df_final.data_main(data)
        st.dataframe(to_send, use_container_width=True)
        csv = convert_df(to_send)
        st.download_button("📥 Download file", data=csv, file_name=f"{today_str}.csv", mime='text/csv')

    user_input = st.text_area("Enter lotto bets here:", placeholder="""Please follow format:
text1
1-2-3$10
4-5-6$50

text2
5-6-7$60
7,6.8$70
""", height=400)

    data_ingestion_obj = DataIngestion('numbers.txt')
    data = data_ingestion_obj.text_to_df(user_input)

    buy_back_bonus_toggle, buy_back_3n_toggle = st.columns(2)
    with buy_back_bonus_toggle:
        buy_back_bonus = st.number_input('Buy Back Bonus', value=100, key='buy_back_bonus')
    with buy_back_3n_toggle:
        buy_back_3n = st.number_input('Buy Back 3n', value=50, key='buy_back_3n')

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    if col1.button("Submit", key="submit_button"):
        df_final = DataFinal()
        to_send, buy_backs = df_final.data_main_3(data)
        st.dataframe(to_send, use_container_width=True)
        csv = convert_df(to_send)
        st.download_button("📥 Download file", data=csv, file_name=f"{today_str}.csv", mime='text/csv')
        st.write('Buy Back Numbers:')
        for row in buy_backs['copy_paste']:
            st.text(row)

    if col2.button("Rearrange", key="rearrange_button"):
        rearr_df = data[data.index != 1000]
        rearr_df[0] = rearr_df[0].astype(int)
        rearr_df['bet'] = rearr_df['bet'].astype(int)
        rearr_df = rearr_df.groupby(0)['bet'].sum().reset_index().sort_values(0)
        rearr_df['copy_paste'] = rearr_df[[0,'bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
        st.text('Bonus')
        for row in rearr_df['copy_paste']:
            st.text(row)

    if col3.button("Only Bonus", key="bonus_button"):
        bonus_df = data[data.index != 1000]
        bonus_df = bonus_df[bonus_df[1] == 0]
        bonus_df[0] = bonus_df[0].astype(int)
        bonus_df['bet'] = bonus_df['bet'].astype(int)
        bonus_df = bonus_df.groupby(0)['bet'].sum().reset_index().sort_values(0)
        bonus_df['copy_paste'] = bonus_df[[0,'bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
        st.text('Bonus')
        for row in bonus_df['copy_paste']:
            st.text(row)

    if col4.button("Only Bonus X2", key='bonus_2x_button'):
        bonus_df = data[data.index != 1000]
        if len(bonus_df.columns) > 2:
            bonus_df = bonus_df[bonus_df[1] == 0]
        bonus_df[0] = bonus_df[0].astype(int)
        bonus_df['bet'] = bonus_df['bet'].astype(int)
        bonus_df = bonus_df.groupby(0)['bet'].sum().reset_index().sort_values(0)
        bonus_df['bet'] *= 2
        bonus_df['copy_paste'] = bonus_df[[0,'bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
        st.text('Bonus')
        for row in bonus_df['copy_paste']:
            st.text(row)

    if col5.button("Buy Back", key='buy_back_button'):
        df_final = DataFinal()
        to_send, buy_backs, additional_buy_back = df_final.data_main_3_buyback(data, buy_back_bonus, buy_back_3n)
        st.dataframe(to_send, use_container_width=True)
        csv = convert_df(to_send)
        st.download_button("📥 Download file", data=csv, file_name=f"{today_str}.csv", mime='text/csv')
        st.write('Buy Back Numbers:')
        for row in buy_backs['copy_paste']:
            if '$' in row and row.split('$')[1]:
                st.text(row)
        st.write('Actual Buy Back')
        for row in buy_backs['actual_buyback_copy_paste']:
            st.text(row)
        for row in additional_buy_back['copy_paste']:
            st.text(row)

    if col6.button("3 Number X2", key="3n_x2"):
        buy_back_3n_x2 = data[data.index != 1000]
        buy_back_3n_x2 = buy_back_3n_x2[buy_back_3n_x2[1] != 0].replace(0, '')
        buy_back_3n_x2['bet'] = buy_back_3n_x2['bet'].astype(int) * 2
        buy_back_3n_x2['bets'] = buy_back_3n_x2.iloc[:,:-1].apply(lambda x: '-'.join(x.dropna().astype(str)), axis=1)
        buy_back_3n_x2['copy_paste'] = buy_back_3n_x2[['bets','bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
        st.text('3 Number X2')
        for row in buy_back_3n_x2['copy_paste']:
            st.text(row)

    if col7.button('Duplicates', key='print_duplicates'):
        duplicates = data[data.index != 1000]
        if len(duplicates.columns) > 4:
            duplicates = duplicates[(duplicates[3] == 0) & (duplicates[1] != 0) & (duplicates[2] != 0)]
        df_dup = duplicates[duplicates.duplicated(subset=[0,1,2], keep=False)]
        df_dup['bet'] = df_dup['bet'].astype(int)
        df_dup = df_dup.replace(0,'')
        df_dup['bets'] = df_dup.iloc[:,:-1].apply(lambda x: '-'.join(x.dropna().astype(str)), axis=1)
        df_dup['copy_paste'] = df_dup[['bets','bet']].apply(lambda x: '-$'.join(x.astype(str)), axis=1)
        st.text('Duplicates:')
        for row in df_dup['copy_paste'].sort_values():
            st.text(row)

    return data

def winning_numbers():
    st.subheader("🏅 Check Against Winning Numbers")
    lotto_names = ['Megadice','Daily Grand','Lotto 6/49', 'Lotto Max']
    selected_lotto = st.selectbox('🎰 Choose Lotto', lotto_names)
    user_input = st.text_area("Enter numbers to check here:", placeholder="""Please follow format:
text1
1-2-3$10
4-5-6$50

text2
5-6-7$60
7,6.8$70
""", height=400)

    data_ingestion_obj = DataIngestion('numbers.txt')
    data = data_ingestion_obj.text_to_df(user_input)

    if st.button("🔍 Check"):
        date, winning_nums, bs = scrape_winning_nums(selected_lotto)
        st.write(date)
        st.write(', '.join(str(num) for num in winning_nums) + ' bonus ' + str(bs))
        winners = check_winning_nums(data, winning_nums, bs)
        st.write(winners)

def main():
    tz = pytz.timezone('US/Eastern')
    today = datetime.now(tz)
    today_str = today.strftime('%B-%d-%Y')
    st.set_page_config(page_title="Uncle Kevin Lotto App", page_icon="🎯")
    st.title(f"🎯 Uncle Kevin Lotto App")
    st.caption(f"Today's Date: {today_str}")

    tab1, tab2, tab3, tab4 = st.tabs(['📝 Submit Bets', '🏆 Check Winning Numbers', '📦 Uncle Kevin Bets', '📊 Master Data'])
    with tab1:
        main_2()
    with tab2:
        winning_numbers()
    with tab3:
        main_3()
    with tab4:
        st.write('📌 TBD: Coming Soon')

if __name__ == "__main__":
    main()
