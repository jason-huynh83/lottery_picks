import streamlit as st
from src.components.data_ingestion import DataIngestion
from src.components.data_run import DataFinal
from datetime import datetime
from src.utils import check_winning_nums, scrape_winning_nums
import pytz
import pandas as pd
import plotly.graph_objects as go

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

YEARS_DEFAULT = (2024, 2025)

# ---------- Shared helpers ----------
def _prep_overall_pivot(df: pd.DataFrame, years=YEARS_DEFAULT):
    """Prepare month-day aligned cumulative pivot for overall (all rows)."""
    d = df.copy()
    d["Day"] = pd.to_datetime(d["Day"])
    d["Year"] = d["Day"].dt.year
    d["MonthDay"] = d["Day"].dt.strftime("%m-%d")
    d = d[d["Year"].isin(years)].copy()
    d = d[d["MonthDay"] != "02-29"]  # drop leap day

    daily = (
        d.groupby(["Year", "Day"], as_index=False)["Earnings"]
         .sum()
         .sort_values(["Year", "Day"])
    )
    daily["CumEarnings"] = daily.groupby("Year")["Earnings"].cumsum()
    daily["MonthDay"] = daily["Day"].dt.strftime("%m-%d")

    pivot = (
        daily.pivot_table(index="MonthDay", columns="Year", values="CumEarnings", aggfunc="last")
             .sort_index()
    )

    # full calendar index (no Feb 29)
    all_md = pd.date_range("2000-01-01", "2000-12-31", freq="D")
    all_md = all_md[~((all_md.month == 2) & (all_md.day == 29))]
    all_idx = all_md.strftime("%m-%d")
    pivot = pivot.reindex(all_idx)

    y_prev, y_cur = min(years), max(years)
    pivot["YoY_Diff"] = pivot.get(y_cur) - pivot.get(y_prev)

    # x-axis with dummy year for clean month labels
    x_dt = pd.to_datetime("2000-" + pivot.index)
    return x_dt, pivot, y_prev, y_cur


def _prepare_pivot_for_dim(df_in: pd.DataFrame, dim_col: str, dim_value, years=YEARS_DEFAULT):
    """Prepare month-day aligned cumulative pivot for a single dim value (e.g., Weekday='Mon')."""
    d = df_in.copy()
    d["Day"] = pd.to_datetime(d["Day"])
    d["Year"] = d["Day"].dt.year
    d["MonthDay"] = d["Day"].dt.strftime("%m-%d")
    d = d[(d[dim_col] == dim_value) & (d["Year"].isin(years))].copy()
    if d.empty:
        return None, None, None, None

    d = d[d["MonthDay"] != "02-29"]

    daily = (
        d.groupby(["Year", "Day"], as_index=False)["Earnings"]
         .sum()
         .sort_values(["Year", "Day"])
    )
    if daily.empty:
        return None, None, None, None

    daily["CumEarnings"] = daily.groupby("Year")["Earnings"].cumsum()
    daily["MonthDay"] = daily["Day"].dt.strftime("%m-%d")

    pivot = (
        daily.pivot_table(index="MonthDay", columns="Year", values="CumEarnings", aggfunc="last")
             .sort_index()
    )

    all_md = pd.date_range("2000-01-01", "2000-12-31", freq="D")
    all_md = all_md[~((all_md.month == 2) & (all_md.day == 29))]
    idx = all_md.strftime("%m-%d")
    pivot = pivot.reindex(idx)

    # start at 0 then forward-fill within each year
    y_prev, y_cur = min(years), max(years)
    for y in years:
        if y not in pivot.columns:
            pivot[y] = np.nan
        if pd.isna(pivot.iloc[0][y]):
            pivot.iloc[0, pivot.columns.get_loc(y)] = 0.0
        pivot[y] = pivot[y].ffill()

    pivot["YoY_Diff"] = pivot[y_cur] - pivot[y_prev]
    x_dt = pd.to_datetime("2000-" + pivot.index)
    return x_dt, pivot, y_prev, y_cur


# ---------- Public: figures you can call in tab4 ----------
def make_yoy_overlay_fig(df: pd.DataFrame, years=YEARS_DEFAULT, title_prefix="Running Totals of Earnings — YoY Overlay"):
    """Overall 2024 vs 2025 overlay + YoY Δ on secondary axis. Returns a Plotly Figure."""
    x_dt, pivot, y_prev, y_cur = _prep_overall_pivot(df, years=years)

    fig = go.Figure()
    if y_prev in pivot.columns:
        fig.add_trace(go.Scatter(
            x=x_dt, y=pivot[y_prev], mode="lines", name=str(y_prev),
            hovertemplate="%{x|%b %d}: $" + "%{y:,.0f}<extra>" + str(y_prev) + "</extra>"
        ))
    if y_cur in pivot.columns:
        fig.add_trace(go.Scatter(
            x=x_dt, y=pivot[y_cur], mode="lines", name=str(y_cur),
            hovertemplate="%{x|%b %d}: $" + "%{y:,.0f}<extra>" + str(y_cur) + "</extra>"
        ))
    fig.add_trace(go.Scatter(
        x=x_dt, y=pivot["YoY_Diff"], mode="lines",
        name=f"YoY Δ ({y_cur}-{y_prev})",
        line=dict(dash="dot"),
        yaxis="y2",
        hovertemplate="%{x|%b %d}: $" + "%{y:,.0f}<extra>YoY Δ</extra>"
    ))

    fig.update_layout(
        title=f"{title_prefix} ({y_cur} vs {y_prev})",
        xaxis=dict(title="Month", tickformat="%b", rangeslider=dict(visible=True)),
        yaxis=dict(title="Cumulative Earnings"),
        yaxis2=dict(title="YoY Δ (Cumulative)", overlaying="y", side="right", showgrid=False),
        legend=dict(title="Series"),
        hovermode="x unified",
        margin=dict(l=70, r=70, t=80, b=50),
        height=600,
    )
    return fig


def make_yoy_dropdown_by_weekday(df: pd.DataFrame, years=YEARS_DEFAULT,
                                 title_prefix="Running Totals — YoY Overlay"):
    """Dropdown to toggle each Weekday; shows prev year, current year, and YoY Δ."""
    values = [v for v in sorted(df["Weekday"].dropna().unique())]
    traces, valid_values = [], []
    for i, val in enumerate(values):
        res = _prepare_pivot_for_dim(df, "Weekday", val, years=years)
        x_dt, pv, y_prev, y_cur = res
        if pv is None:
            continue
        valid_values.append(val)
        first = (len(valid_values) == 1)
        traces.extend([
            go.Scatter(x=x_dt, y=pv[y_prev], mode="lines", name=f"{y_prev}", visible=first),
            go.Scatter(x=x_dt, y=pv[y_cur],  mode="lines", name=f"{y_cur}",  visible=first),
            go.Scatter(x=x_dt, y=pv["YoY_Diff"], mode="lines",
                       name=f"YoY Δ ({y_cur}-{y_prev})", line=dict(dash="dot"),
                       visible=first, yaxis="y2"),
        ])
    if not valid_values:
        raise ValueError("No data for Weekday dropdown.")

    # visibility masks (3 traces per option)
    def vis_mask(idx):
        return sum(([i == idx]*3 for i in range(len(valid_values))), [])

    buttons = [
        dict(
            label=str(val),
            method="update",
            args=[{"visible": vis_mask(i)},
                  {"title": f"{title_prefix} ({years[1]} vs {years[0]}) — Weekday: {val}"}],
        )
        for i, val in enumerate(valid_values)
    ]

    fig = go.Figure(traces)
    fig.update_layout(
        title=f"{title_prefix} ({years[1]} vs {years[0]}) — Weekday: {valid_values[0]}",
        xaxis=dict(tickformat="%b", title="Month"),
        yaxis=dict(title="Cumulative Earnings"),
        yaxis2=dict(title="YoY Δ (Cumulative)", overlaying="y", side="right", showgrid=False),
        legend=dict(title="Series"),
        hovermode="x unified",
        updatemenus=[dict(type="dropdown", x=1.02, xanchor="left", y=1.10, yanchor="top",
                          buttons=buttons, direction="down", showactive=True)],
        margin=dict(l=70, r=70, t=80, b=50),
        height=600,
    )
    return fig


def make_yoy_dropdown_by_lotto_type(df: pd.DataFrame, years=YEARS_DEFAULT,
                                    title_prefix="Running Totals — YoY Overlay"):
    """Dropdown to toggle each lotto_type; shows prev year, current year, and YoY Δ."""
    values = [v for v in sorted(df["lotto_type"].dropna().unique())]
    traces, valid_values = [], []
    for i, val in enumerate(values):
        res = _prepare_pivot_for_dim(df, "lotto_type", val, years=years)
        x_dt, pv, y_prev, y_cur = res
        if pv is None:
            continue
        valid_values.append(val)
        first = (len(valid_values) == 1)
        traces.extend([
            go.Scatter(x=x_dt, y=pv[y_prev], mode="lines", name=f"{y_prev}", visible=first),
            go.Scatter(x=x_dt, y=pv[y_cur],  mode="lines", name=f"{y_cur}",  visible=first),
            go.Scatter(x=x_dt, y=pv["YoY_Diff"], mode="lines",
                       name=f"YoY Δ ({y_cur}-{y_prev})", line=dict(dash="dot"),
                       visible=first, yaxis="y2"),
        ])
    if not valid_values:
        raise ValueError("No data for lotto_type dropdown.")

    def vis_mask(idx):
        return sum(([i == idx]*3 for i in range(len(valid_values))), [])

    buttons = [
        dict(
            label=str(val),
            method="update",
            args=[{"visible": vis_mask(i)},
                  {"title": f"{title_prefix} ({years[1]} vs {years[0]}) — lotto_type: {val}"}],
        )
        for i, val in enumerate(valid_values)
    ]

    fig = go.Figure(traces)
    fig.update_layout(
        title=f"{title_prefix} ({years[1]} vs {years[0]}) — lotto_type: {valid_values[0]}",
        xaxis=dict(tickformat="%b", title="Month"),
        yaxis=dict(title="Cumulative Earnings"),
        yaxis2=dict(title="YoY Δ (Cumulative)", overlaying="y", side="right", showgrid=False),
        legend=dict(title="Series"),
        hovermode="x unified",
        updatemenus=[dict(type="dropdown", x=1.02, xanchor="left", y=1.10, yanchor="top",
                          buttons=buttons, direction="down", showactive=True)],
        margin=dict(l=70, r=70, t=80, b=50),
        height=600,
    )
    return fig
def lotto_type(weekday):
    if weekday == 'Wednesday' or weekday == 'Saturday':
        return 'md/649'
    elif weekday == 'Thursday' or weekday == 'Monday':
        return 'md/grand'
    elif weekday == 'Friday' or weekday == 'Tuesday':
        return 'md/max'
    elif weekday == 'Sunday':
        return 'md'
    else:
        return None
    
def load_master_from_public_gsheet(spreadsheet_id: str, gid: str) -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)


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
        df = load_master_from_public_gsheet("11UQYJadXLZ-ZwE-7mqTDX5tfkPgyJUH0ZLyodTViTLM", "2075169032")
        df = df.copy()
        df["Day"] = pd.to_datetime(df["Day"], errors="coerce")

        # robust currency-to-float cleaner
        df["Earnings"] = (
            df["Earnings"]
            .astype(str)
            .str.replace(r"[^\d\-\.\(\)]", "", regex=True)      # strip $, commas, spaces
            .str.replace(r"^\((.*)\)$", r"-\1", regex=True)      # (123.45) -> -123.45
        )
        df["Earnings"] = pd.to_numeric(df["Earnings"], errors="coerce").fillna(0.0)
        df['lotto_type'] = df['Weekday'].apply(lotto_type)
        st.subheader("YoY Overview")
        fig_overall = make_yoy_overlay_fig(df, years=(2024, 2025))
        st.plotly_chart(fig_overall, use_container_width=True)

        st.subheader("YoY by Weekday")
        fig_weekday = make_yoy_dropdown_by_weekday(df, years=(2024, 2025))
        st.plotly_chart(fig_weekday, use_container_width=True)

        st.subheader("YoY by lotto_type")
        fig_lotto = make_yoy_dropdown_by_lotto_type(df, years=(2024, 2025))
        st.plotly_chart(fig_lotto, use_container_width=True)

if __name__ == "__main__":
    main()
