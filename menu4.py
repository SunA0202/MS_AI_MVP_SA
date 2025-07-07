import sqlite3
import streamlit as st
import graphviz
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
import matplotlib.pyplot as plt
import cv2


def menu4_ui():
    """
    Streamlit UI for displaying SQLite ERD based on foreign key relationships.
    """
    st.write("SQLite ERD (Foreign Key 관계도)")
    # DB 연결
    conn = sqlite3.connect("./DB/OWN2.db")
    cursor = conn.cursor()

    # 테이블 목록 조회
    cursor.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    tables = [row[0] for row in cursor.fetchall()]

    # FK 정보 수집
    relations = []
    table_columns = {}

    for table in tables:
        # 테이블의 FK 리스트
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        fks = cursor.fetchall()

        for fk in fks:
            # fk[2] : 참조 테이블 이름
            # fk[3] : from 컬럼
            # fk[4] : to 컬럼
            relations.append({
                "from_table": table,
                "from_column": fk[3],
                "to_table": fk[2],
                "to_column": fk[4],
            })

        # 테이블의 컬럼 정보 (node label로 표시)
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in cursor.fetchall()]
        table_columns[table] = columns

    # Streamlit 화면
    st.title("📘 SQLite ERD (Foreign Key 관계도)")

    # Graphviz 객체 생성
    dot = graphviz.Digraph(engine="dot")

    # 테이블 노드 추가
    for table, columns in table_columns.items():
        label = f"{table}|{'|'.join(columns)}"
        dot.node(table, label="{" + label + "}", shape="record")

    # FK 관계 선 추가
    for rel in relations:
        dot.edge(
            rel["from_table"],
            rel["to_table"],
            label=f"{rel['from_column']} → {rel['to_column']}"
        )

    # 시각화 출력
    st.graphviz_chart(dot)


    # 1. DB 연결
    conn = sqlite3.connect("./DB/OWN2.db")
    cursor = conn.cursor()

    # 2. 테이블명 지정
    table_name = "CUST"  # 원하는 테이블명으로 변경

    # 3. 테이블 정보 조회
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    # 4. DataFrame 생성
    df = pd.DataFrame(columns, columns=["cid", "name", "type", "notnull", "dflt_value", "pk"])
    df_display = df[["name", "type"]]

    print("데이터프레임:\n", df_display)

    # 5. matplotlib로 표 이미지 생성
    fig, ax = plt.subplots(figsize=(6, len(df_display)*0.35))
    ax.axis('off')
    table = ax.table(
        cellText=df_display.values,
        colLabels=df_display.columns,
        loc='center',
        cellLoc='center',
        colColours=['#f2f2f2', '#f2f2f2'],  # 열 헤더 색상
        # edges='open',
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)
    ax.set_title(table_name)
 

    # 바깥쪽 테두리만 그리기
    rows = len(df_display.values) + 1  # +1 for header
    cols = len(df_display.columns)

    for (row, col), cell in table.get_celld().items():
        # 바깥쪽 테두리 구분
        is_top = row == 0
        is_bottom = row == rows - 1
        is_left = col == 0
        is_right = col == cols - 1

        # 기본 테두리 두께
        cell.set_linewidth(1)

        # 셀 테두리 색 결정
        if is_top or is_bottom or is_left or is_right:
            # 외곽선
            cell.set_edgecolor("black")
            cell.set_linewidth(2)
        else:
            # 내부선
            cell.set_edgecolor("blue")
    ax.set_mouseover


    # 6. 이미지로 저장
    output_image = f"{table_name}_schema.png"
    plt.savefig(output_image, bbox_inches='tight', dpi=300)

    print(f"✅ 이미지 저장 완료: {output_image}")

    st.image(output_image, caption=f"{table_name} 테이블 스키마", use_column_width=True)

        # 샘플 데이터
    data = [
        ["Alice", "24"],
        ["Bob", "30"]
    ]
    columns = ["Name", "Age"]

    rows = len(data) + 1  # +1 for header
    cols = len(columns)

    fig, ax = plt.subplots(figsize=(4, 2))
    ax.axis("off")

    # 테이블 생성
    table = ax.table(
        cellText=data,
        colLabels=columns,
        loc="center",
        cellLoc="center"
    )

    # 셀 순회
    for (row, col), cell in table.get_celld().items():
        # 바깥쪽 테두리 구분
        is_top = row == 0
        is_bottom = row == rows - 1
        is_left = col == 0
        is_right = col == cols - 1

        # 기본 테두리 두께
        cell.set_linewidth(1)

        # 셀 테두리 색 결정
        if is_top or is_bottom or is_left or is_right:
            # 외곽선
            cell.set_edgecolor("black")
            cell.set_linewidth(2)
        else:
            # 내부선
            cell.set_edgecolor("blue")

    # 출력
    plt.savefig('temp.png', bbox_inches='tight', dpi=300)

        # 예제 데이터프레임
    df = pd.DataFrame({
        "Column": ["id", "name", "email", "created_at"],
        "Type": ["INTEGER", "TEXT", "TEXT", "DATETIME"]
    })

    # HTML 테이블 + CSS
    def render_hover_table(df):
        # CSS 스타일
        styles = """
        <style>
        table {
            border-collapse: collapse;
            width: 60%;
            margin: 0 auto;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px 12px;
            text-align: center;
        }
        tr:hover {
            background-color: #add8e6; /* 연한 파랑색 */
        }
        th {
            background-color: #f2f2f2;
        }
        </style>
        """

        # DataFrame을 HTML로 변환
        table_html = df.to_html(index=False, escape=False)

        st.markdown(styles + table_html, unsafe_allow_html=True)
        st.write(table_html, unsafe_allow_html=True)

    # Streamlit 앱
    st.title("Table Hover Highlight Example")

    st.write("마우스를 행에 올리면 색상이 변합니다.")
    render_hover_table(df)