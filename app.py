import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd
import menu1, menu2, menu3, menu4

st.set_page_config(page_title="만드는 중", layout="wide")
# st.title('Streamlit 앱의 테마 사용자 정의하기')


# sidebar 설정
menu1_title = "ERD 조회"
menu2_title = "Table Tuning"
menu3_title = "SQL Tuning"
menu4_title = "STREAMLIT TEST"

with st.sidebar:
    choice = option_menu(
        "Menu",
        [menu1_title, menu2_title, menu3_title, menu4_title],
        icons=['house', 'kanban', 'bi bi-robot'],
        menu_icon="app-indicator",
        default_index=0,
        styles={
            "container": {"padding": "4!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#08c7b4"},
        }
    )

if choice == menu1_title:
    st.header(menu1_title)
    menu1.menu1_ui()
elif choice == menu2_title:
    st.header(menu2_title)
    menu2.menu2_ui()
elif choice == menu3_title:
    st.header(menu3_title)
    st.write("입력된 SQL을 OPEN AI를 통해 튜닝하고, EXPLAIN PLAN을 통해 성능을 분석 >> 튜닝하는 핵심 기능 구현 필요")
    menu3.menu3_ui()
elif choice == menu4_title:
    st.header(menu4_title)
    menu4.menu4_ui()