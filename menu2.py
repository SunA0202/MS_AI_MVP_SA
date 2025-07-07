import streamlit as st
import pandas as pd
import datetime

def menu2_ui():

    col1, col2 = st.columns(2)
    # 오늘 날짜를 기본값으로 설정
    with col1:
        tuning_button = st.button("Table Tuning")
        col11, col12 = st.columns(2)
        today = datetime.date.today()
        # 날짜 2개 따로 입력
        start_date = col11.date_input("시작 날짜", today-datetime.timedelta(days=30))
        end_date = col12.date_input("종료 날짜", today)

        # 유효성 검사
        if start_date > end_date:
            st.error("❌ 시작 날짜는 종료 날짜보다 앞서야 합니다.")
        else:
            st.success(f"선택한 기간: {start_date} ~ {end_date}")

        if tuning_button:
            st.write("Table Tuning 버튼이 클릭되었습니다.")