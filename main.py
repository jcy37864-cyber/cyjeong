import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 및 세션 초기화 =================
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

# 변수 초기화 (AttributeError 방지용 안전 설계)
defaults = {
    "stage": 0,
    "survive": 0,
    "fail": 0,
    "heart": 0,
    "safe_choice": random.randint(0, 2),
    "heart_choice": random.randint(0, 2),
    "loading_done": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ================= 2. 🎨 분위기별 디자인 설정 =================
def apply_theme():
    # 스테이지 4(반전)부터는 화이트 배경, 그 전엔 블랙 배경
    if st.session_state.stage >= 4:
        bg, text, accent, btn_bg = "#FFFFFF", "#333333", "#FF4B4B", "#FFF0F0"
    else:
        bg, text, accent, btn_bg = "#000000", "#FF0000", "#8B0000", "#1A1A1A"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; transition: all 1.5s ease; }}
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {accent} !important;
        border: 2px solid {accent} !important;
        border-radius: 15px;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
    }}
    .center {{ text-align: center; }}
    .big-text {{ font-size: 35px; font-weight: bold; margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 🖼️ 특수 효과 함수 =================
def play_audio(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', unsafe_allow_html=True)

def show_img(file_name):
    if os.path.exists(file_name):
        st.image(file_name, use_container_width=True)

def typewriter(text, speed=0.06):
    """한 글자씩 출력하며 몰입감 유도"""
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f'<div class="center" style="font-size:20px;">{displayed_text}</div>', unsafe_allow_html=True)
        time.sleep(speed)

# ================= 4. 메인 게임 로직 =================

# --- [Stage 0] 입장 및 20초 카운트다운 ---
if st.session_state.stage
