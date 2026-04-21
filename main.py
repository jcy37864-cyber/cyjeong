import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 및 세션 상태 초기화 =================
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

if "stage" not in st.session_state:
    st.session_state.update({
        "stage": 0,
        "survive": 0,
        "fail": 0,
        "heart": 0,
        "safe_choice": random.randint(0, 2),
        "heart_choice": random.randint(0, 2),
        "loading_done": False
    })

# ================= 2. 🎨 분위기별 동적 스타일 =================
def apply_theme():
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
        transition: 0.3s;
    }}
    div.stButton > button:hover {{ transform: scale(1.02); background-color: {accent} !important; color: white !important; }}
    .center {{ text-align: center; }}
    .big-text {{ font-size: 38px; font-weight: bold; margin-bottom: 20px; font-family: 'Courier New', Courier, monospace; }}
    .typewriter {{ font-size: 20px; line-height: 1.6; font-family: 'Courier New', Courier, monospace; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 🖼️ 유틸리티 함수 =================
def play_audio(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            b64 = base64.base64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', unsafe_allow_html=True)

def show_img(file_name):
    if os.path.exists(file_name):
        st.image(file_name, use_container_width=True)

def typewriter(text, speed=0.05):
    """한 글자씩 출력되는 효과 (시간 끌기용)"""
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f'<div class="center typewriter">{displayed_text}</div>', unsafe_allow_html=True)
        time.sleep(speed)

# ================= 4. 게임 스테이지별 실행 로직 =================

# --- [0] 시작화면 (20초 카운트다운 추가) ---
if st.session_state.stage == 0:
    st.markdown('<div class="center big-text">👁️ WARNING</div>', unsafe_allow_html=True)
    st.markdown('<div class="center info-text">게임을 좋아하는 이소연... <br>허락 없이 들어온 대가는 가혹할 거야.</div>', unsafe_allow_html=True)
    
    if not st.session_state.loading_done:
        if st.button("운명을 확인하기 (보안 검사 필요)"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 20초간 시간 끌기
            messages = [
                "신원 파악 중...", "이소연... 접속 기록 확인됨...", 
                "심박수 측정 중...", "도망칠 기회를 계산 중...", 
                "주변 환경 스캔 중...", "거의 다 왔어...", 
                "준비해. 이제 시작이야."
            ]
            
            for i in range(101):
                time.sleep(0.2)  # 약 20초 (0.2 * 100)
                progress_bar.progress(i)
                if i % 15 == 0:
                    status_text.markdown(f'<div class="center">{random.choice(messages)}</div>', unsafe_allow_html=True)
            
            st.session_state.loading_done = True
            st.rerun()
    else:
        st.success("접속 승인됨. 아래 버튼을 눌러 입장해.")
        if st.button("지옥의 문 열기"):
            st.session_state.stage = 1
            st.rerun()

# --- [1] 공포의 서막 (타이핑 효과 적용) ---
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center big-text">누군가 널 지켜보고 있어...</div>', unsafe_allow_html=True)
    show_img("scary.jpg")
    typewriter("...으악! 방금 뒤에서 소리 들리지 않았어? 소연아, 절대 뒤돌아보지 마.")
    
    if st.button("도망치기 위해 계속 가기"):
        st.session_state.stage = 2
        st.rerun()

# --- [2] 생존 선택 게임 (시련 강화) ---
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    # 목표를 3회에서 5회로 상향
    st.markdown(f'<div class="center big-text">죽음의 선택 ({st.session_state.survive}/5)</div>', unsafe_allow_html=True)
    
    if random.random() > 0.8: show_img("jumpscare.jpg")
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"문 {i+1}", key=f"door_{i}"):
                if i == st.session_state.safe_choice:
                    st.session_state.survive += 1
                    st.toast("...희망이 보여...")
                else:
                    st.session_state.fail += 1
                    st.toast("크크큭... 틀렸어.....")
                st.session_state.safe_choice = random.randint(0, 2)
                st.rerun()

    if st.session_state.fail >= 3:
        st.error("영원히 이곳에 갇혔습니다....")
        if st.button("영혼을 바쳐 다시 시도"):
            st.session_state.clear()
            st.rerun()
    
    if st.session_state.survive >= 5:
        if st.button("희미한 빛이 보이는 곳으로 탈출"):
            st.session_state.stage = 3
            st.rerun()

# --- [3] 마지막 심리전 ---
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center big-text">자, 이제 마지막이다...</div>', unsafe_allow_html=True)
    show_img("scary2.jpg")
    typewriter("너는 정말로 나를 믿어? 이 모든 게 우연이라고 생각해?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("믿는다"):
            st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("절대 못 믿어"):
            st.markdown('<h1 class="center">💥 공격 당했습니다 💥</h1>', unsafe_allow_html=True)
            time.sleep(2)
            st.session_state.clear()
            st.rerun()

# --- [4] 반전 ---
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center big-text" style="color:#FF4B4B;">🎉 Surprise! 🎉</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    typewriter("소연아 무서웠지? 미안해! 사실 널 위해 준비한 작은 이벤트야!")
    if st.button("내 진심을 확인해줄래?"):
        st.session_state.stage = 5
        st.rerun()

# --- [5] 하트 잡기 게임 ---
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center big-text" style="color:#FF4B4B;">내 마음을 잡아줘 💖</div>', unsafe_allow_html=True)
    st.progress(st.session_state.heart / 5)
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i == st.session_state.heart_choice:
                if st.button("💖", key=f"heart_btn_{i}"):
                    st.session_state.heart += 1
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()
            else:
                if st.button("🤍", key=f"empty_btn_{i}"):
                    st.toast("빗나갔어!")
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()

    if st.session_state.heart >= 5:
        st.markdown("---")
        # 여기서 시간을 한 번 더 끕니다.
        if st.button("모든 마음을 모았어! 클릭! ✨"):
            with st.spinner("진심을 전하기 위해 용기를 내는 중..."):
                time.sleep(5) # 5초 대기
            st.session_state.stage = 6
            st.rerun()

# --- [6] 최종 고백 ---
elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center big-text">사실은 말이야...</div>', unsafe_allow_html=True)
    typewriter("소연씨, 나랑 함께하면서 더 많은 축복을 나누고 영원히 함께해주지 않을래? 🌹", speed=0.1)
    if st.button("YES! 나도 좋아 💖"):
        st.session_state.stage = 7
        st.rerun()

# --- [7] 엔딩 ---
elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3")
    st.balloons()
    st.markdown('<div class="center big-text" style="color:#FF4B4B;">우리 사랑 영원히 💖</div>', unsafe_allow_html=True)
    show_img("final.jpg")
    st.markdown('<div class="center info-text">위의 사진(QR)을 확인해봐! 우리의 새로운 시작이야.</div>', unsafe_allow_html=True)
    
    if st.button("처음으로 돌아가기"):
        st.session_state.clear()
        st.rerun()
