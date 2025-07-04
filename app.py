# streamlit_example.py
import streamlit as st

# Title of the app
st.title("Streamlit 간단한 예제")

# Input text box
name = st.text_input("이름을 입력하세요:")

# Slider for age
age = st.slider("나이를 선택하세요:", 0, 100, 25)

# Button to submit
if st.button("제출"):
    st.write(f"안녕하세요, {name}님! 당신의 나이는 {age}살입니다.")

# Checkbox example
if st.checkbox("추가 정보를 표시"):
    st.write("Streamlit은 Python으로 웹 앱을 쉽게 만들 수 있는 라이브러리입니다!")