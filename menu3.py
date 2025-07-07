import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd


def menu3_ui():
    st.write("아래에 SQL문을 입력하고 실행해보세요.")

    col1, col2 = st.columns(2)
    with col1:
        # 서브 열
        col11,col12,col13,col13,col13  = st.columns(5)
        with col11:
            plan_button = st.button("EXPLAIN PLAN")
        with col12:
            tunuing_button = st.button("SQL Tuning")
        input_query = st.text_area("SQL문 입력","SELECT * FROM CUST", height=300)

    with col2:
        st.button(" ")
        tuned_query = st.text_area("Tuned SQL", "SELECT * FROM CONT", height=300)


    if plan_button:
        try:
            # 인메모리 DB 연결
            conn = sqlite3.connect('DB/OWN2.db')
            c = conn.cursor()
            input_query = "EXPLAIN QUERY PLAN " + input_query
            c.execute(input_query)

            global query1_plan
            query1_plan = pd.DataFrame(c.fetchall(), columns=["ID", "Parent", "Not Used", "Detail"])
            with col1:
                st.write("결과:")
                st.dataframe(query1_plan)
        except Exception as e:
            st.error(f"에러: {e}")


    if tunuing_button:
        # 해당 버튼 클릭시 sql_query를 OPEN AI를 통해 튜닝하고 화면에 노출
        # 튜닝된 쿼리 플랜까지 보여주기
        try:
            # 인메모리 DB 연결
            conn = sqlite3.connect('DB/OWN2.db')
            c = conn.cursor()
            tuned_query = "EXPLAIN QUERY PLAN " + tuned_query
            c.execute(tuned_query)
            query2_plan = pd.DataFrame(c.fetchall(), columns=["ID", "Parent", "Not Used", "Detail"])

            with col1:
                st.write("결과:")
                st.dataframe(query1_plan)

            with col2:
                st.write("결과:")
                st.dataframe(query2_plan)
        except Exception as e:
            st.error(f"에러: {e}")