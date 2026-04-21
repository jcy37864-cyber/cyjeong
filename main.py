import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 현재 폴더 위치 확인
current_path = os.path.dirname(os.path.abspath(__file__))

# 1. HTML 파일 읽기
with open("confession_game.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 2. 파이썬 실행창에 HTML 띄우기
# (참고: 로컬 이미지는 보안상 웹브라우저에서 바로 안 보일 수 있어요. 
# 그럴 땐 HTML 파일을 그냥 더블클릭해서 크롬으로 여는 게 가장 확실하긴 합니다!)
st.components.v1.html(html_content, height=800, scrolling=True)

st.info("💡 이미지가 여전히 안 나온다면? 모든 이미지 파일이 'main.py'와 같은 폴더에 있는지 확인해주세요!")
