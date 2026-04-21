import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 및 세션 초기화 =================
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

# 초기 변수 설정 (AttributeError 방어)
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

# ================= 2. 🎨 디자인 테마 설정 =================
def apply_theme():
    # 스테이지 4(반전)부터 화이트 배경, 그 전엔 블랙 배경
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

# ================= 3. 🖼️ 미디어 및 특수효과 함수 =================
def play_audio(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', unsafe_allow_html=True)

def show_img(file_name):
    if os.path.exists(file_name):
        st.image(file_name, use_container_width=True)

def typewriter(text, speed=0.05):
    """한 글자씩 출력하며 시간 끌기"""
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f'<div class="center" style="font-size:20px;">{displayed_text}</div>', unsafe_allow_html=True)
        time.sleep(speed)

# ================= 4. 게임 스테이지 로직 =================

# --- [Stage 0] 시작 & 20초 카운트다운 ---
if st.session_state.stage == 0:
    st.markdown('<div class="center big-text">👁️ ACCESS DENIED</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">이소연님, 허락 없이 들어온 대가는 가혹할 거야.</div>', unsafe_allow_html=True)
    
    if not st.session_state.loading_done:
        if st.button("권한 요청 (ID: 이소연)"):
            bar = st.progress(0)
            status = st.empty()
            messages = ["서버 연결...", "데이터 분석 중...", "심박수 측정...", "보안 해제 중...", "거의 다 됨..."]
            for i in range(101):
                time.sleep(0.15) # 0.15 * 100 = 약 15~20초
                bar.progress(i)
                if i % 20 == 0:
                    status.markdown(f'<div class="center">{messages[i//20 % len(messages)]}</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True
            st.rerun()
    else:
        st.warning("⚠️ 접속이 승인되었습니다.")
        if st.button("깊은 곳으로 들어가기"):
            st.session_state.stage = 1
            st.rerun()

# --- [Stage 1] 공포 서막 ---
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center big-text">누군가 널 지켜보고 있어...</div>', unsafe_allow_html=True)
    show_img("scary.jpg")
    typewriter("방금 소리 들었어? 뒤돌아보지 말고 계속 가...")
    if st.button("도망치기 위해 계속 가기"):
        st.session_state.stage = 2
        st.rerun()

# --- [Stage 2] 생존 게임 (5번 성공) ---
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center big-text">살고 싶어? ({st.session_state.survive}/5)</div>', unsafe_allow_html=True)
    if random.random() > 0.8: show_img("jumpscare.jpg")
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"문 {i+1}", key=f"d{i}"):
                if i == st.session_state.safe_choice:
                    st.session_state.survive += 1
                    st.toast("운이 좋군...")
                else:
                    st.session_state.fail += 1
                    st.toast("틀렸어!")
                st.session_state.safe_choice = random.randint(0, 2)
                st.rerun()
                
    if st.session_state.fail >= 3:
        st.error("죽음이 찾아왔습니다.")
        if st.button("다시 도전"):
            st.session_state.clear()
            st.rerun()
    if st.session_state.survive >= 5:
        if st.button("탈출구로 뛰기"):
            st.session_state.stage = 3
            st.rerun()

# --- [Stage 3] 마지막 질문 ---
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center big-text">정말 나를 믿어?</div>', unsafe_allow_html=True)
    show_img("scary2.jpg")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("믿는다"):
            st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("못 믿는다"):
            st.markdown('<h1 class="center">💥 폭파됨 💥</h1>', unsafe_allow_html=True)
            if st.button("부활"): st.session_state.clear(); st.rerun()

# --- [Stage 4] 반전 (하얀 배경) ---
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center big-text" style="color:#FF4B4B;">🎉 놀랐지? 🎉</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    typewriter("소연아 미안해! 사실 널 위해 준비한 서프라이즈야. 무서운 거 아니니까 안심해!")
    if st.button("내 진심을 확인해볼래?"):
        st.session_state.stage = 5
        st.rerun()

# --- [Stage 5] 하트 잡기 ---
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center big-text" style="color:#FF4B4B;">내 마음을 받아줘 💖 ({st.session_state.heart}/5)</div>', unsafe_allow_html=True)
    st.progress(
