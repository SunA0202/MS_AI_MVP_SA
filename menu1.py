import sqlite3
import streamlit as st
import graphviz
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

def menu1_ui():


    st.title("📊 SQLite ERD with streamlit-agraph")
    col1, col2 = st.columns(2) 

    # DB 연결
    conn = sqlite3.connect("./DB/OWN2.db")
    cursor = conn.cursor()

    # 1. 테이블 목록 조회 (sqlite 시스템 테이블 제외)
    cursor.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """)
    tables = [row[0] for row in cursor.fetchall()]

    # 2. 테이블 컬럼, FK 정보 수집
    edges = []

    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        fks = cursor.fetchall()
        for fk in fks:
            # fk 구조: (id, seq, table, from, to, on_update, on_delete, match)
            # from: FK가 걸린 컬럼 (현재 테이블)
            # table: 참조 테이블 이름
            # to: 참조 테이블 컬럼
            edges.append(Edge(source=table, target=fk[2], label=f"FK", font={"size": 13, "face": "arial", "color": "red"}))
            

    # 3. 노드 생성 (테이블명 + 컬럼 나열)
    nodes = []
    for table in tables:
        label = f"{table}\n"
        nodes.append(Node(id=table, label=label, font={"size": 16, "face": "arial", "color": "black", "bold": True, "vadjust": -100}))
 
    # 4. 그래프 설정
    config = Config(
        width=500,
        height=600,
        directed=True,
        nodeHighlightBehavior=True,
        highlightColor="#f0a500",
        collapsible=False,
        physics=False,  # False이면 고정
        hierarchical={
            "enabled": True,
            "direction": "LR",   # UD: 위->아래, LR: 왼->오른
            "sortMethod": "directed"
        },
        layout={
            "hierarchical": True
        },
        node={
            "labelProperty": "label",
            "fontSize": 12,
        },
        edge={
            "labelProperty": "label",
            "fontSize": 10,
        }
    )

    with col1: 
        # 5. 그래프 출력
        global selected
        selected = agraph(nodes=nodes, edges=edges, config=config) 

    with col2:
        # node 클릭시 해당 테이블의 스키마 출력
        st.write("선택된 테이블:", selected) 
        cursor.execute(f"PRAGMA table_info({selected})")
        schem = cursor.fetchall()

        schem = pd.DataFrame(schem, columns=["cid", "name", "type", "notnull", "dflt_value", "pk"])

        cursor.execute(f"PRAGMA index_list({selected})")
        idxs = cursor.fetchall()
        idxs = pd.DataFrame(idxs)

        if selected:
            st.write("테이블 스키마") 
            render_hover_table(schem) 
            st.write("인덱스 목록") 
            render_hover_table(idxs) 



def render_hover_table(df): 
    # CSS 스타일
    styles = """
    <style>
    table {
        border-collapse: collapse;
        width: 60%;
        margin: 0 auto;
        margin-left: 0;
    }
    th {
        background-color: #f2f2f2;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 8px 12px;
        text-align: center !important;
    }
    tr:hover {
        background-color: #add8e6; /* 연한 파랑색 */
    }

    </style>
    """

    # DataFrame을 HTML로 변환
    table_html = df.to_html(index=False, escape=False)

    st.markdown(styles, unsafe_allow_html=True)
    st.write(table_html, unsafe_allow_html=True)
