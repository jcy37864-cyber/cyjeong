import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 1. 파일을 바이트로 읽어서 HTML이 인식할 수 있는 텍스트로 바꾸는 함수
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# 2. HTML 파일 읽기
with open("confession_game.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 3. HTML 안에 있는 파일 이름들을 실제 데이터로 교체하기
# (이 부분이 있어야 사진과 소리가 나옵니다!)
files_to_embed = [
    "scary.jpg", "scary2.jpg", "jumpscare.jpg", "cute.jpg", "final.jpg", "bg.jpg",
    "bgm_scary.mp3", "bgm_love.mp3"
]

for file_name in files_to_embed:
    data_str = get_base64(file_name)
    if data_str:
        # 파일 확장자에 따라 데이터 타입 설정
        ext = file_name.split('.')[-1]
        mime_type = "audio/mpeg" if ext == "mp3" else "image/jpeg"
        # HTML 내의 파일명을 base64 데이터로 치환
        html_content = html_content.replace(file_name, f"data:{mime_type};base64,{data_str}")

# 4. 스트림릿 화면 설정
st.set_page_config(page_title="소연이를 위한 선물", layout="centered")

# 5. 완성된 HTML 띄우기
components.html(html_content, height=900, scrolling=True)
