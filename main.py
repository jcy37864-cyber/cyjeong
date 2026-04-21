import streamlit as st
import streamlit.components.v1 as components

# 화면 꽉 차게 설정
st.set_page_config(layout="wide")

# 1. 소연씨가 가진 HTML 파일을 읽어옵니다.
with open("confession_game.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# 2. 파이썬(Streamlit) 안에 이 HTML을 통째로 박아넣습니다.
# 높이(height)는 게임 화면에 맞춰 조절하면 됩니다.
components.html(html_code, height=900, scrolling=True)
