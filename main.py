import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 및 세션 초기화 =================
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

# [중요] 세션 변수 안전하게 초기화
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "survive" not in st.session_state:
    st.session_state.survive = 0
if "fail" not in st.session_state:
    st.session_state.fail = 0
if "heart" not in st.session_state:
    st.session_state.heart = 0
if "safe_choice" not in st.session_state:
    st.session_state.safe_choice = random.randint(0, 2)
if "heart_choice" not in st.session_state:
    st.session_state.heart_choice = random.randint(0, 2)
if "loading_done" not in st.session_state:
    st.session_state.loading_done = False
if "trust_count" not in st.session_state:
    st.session_state.trust_count = 0
if "roulette_score" not in st.session_state:
    st.session_state.roulette_score = 0
if "roulette_done" not in st.session_state:
    st.session_state.roulette_done = False
if "dist" not in st.session_state:
    st.session_state.dist = 100
if "current_track" not in st.session_state:
    st.session_state.current_track = None

# ================= 2. 🎨 디자인 및 애니메이션 테마 =================
def apply_theme():
    if st.session_state.stage >= 4:
        bg, text, accent, btn_bg = "#FFFFFF", "#333333", "#FF4B4B", "#FFF0F0"
    else:
        bg, text, accent, btn_bg = "#000000", "#FF0000", "#8B0000", "#1A1A1A"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; transition: all 0.5s ease; }}
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {accent} !important;
        border: 2px solid {accent} !important;
        border-radius: 10px; height: 3.5em; width: 100%; font-weight: bold;
    }}
    @keyframes shake {{
        0% {{ transform: translate(1px, 1px) rotate(0deg); }}
        20% {{ transform: translate(-3px, 0px) rotate(1deg); }}
        40% {{ transform: translate(1px, -1px) rotate(1deg); }}
        60% {{ transform: translate(-3px, 1px) rotate(-1deg); }}
        100% {{ transform: translate(1px, -2px) rotate(-1deg); }}
    }}
    .shake-text {{ display: inline-block; animation: shake 0.2s infinite; color: red; font-size: 30px; font-weight: bold; }}
    .center {{ text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 🎵 오디오 제어 (에러 방지 강화) =================
def play_audio(file_name):
    # 세션 상태에 current_track이 없을 경우를 대비한 안전 코드
    if "current_track" not in st.session_state:
        st.session_state.current_track = None
        
    # 이미 해당 곡이 재생 중이라면 다시 실행하지 않음
    if st.session_state.current_track == file_name:
        return 
    
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.session_state.current_track = file_name
        st.markdown(
            f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', 
            unsafe_allow_html=True
        )

def show_img(file_name):
    if os.path.exists(file_name):
        st.image(file_name, use_container_width=True)

def typewriter(text, speed=0.06):
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f'<div class="center" style="font-size:20px;">{displayed_text}</div>', unsafe_allow_html=True)
        time.sleep(speed)

# ================= 4. 메인 게임 로
