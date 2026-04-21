import streamlit as st
import random
import os
import base64

# ================= 1. 기본 설정 및 상태 관리 =================
st.set_page_config(page_title="???", page_icon="👁️", layout="centered")

if "stage" not in st.session_state:
    st.session_state.update({
        "stage": 0,
        "bgm_started": False,
        "bgm_type": "scary",
        "survive": 0,
        "fail": 0,
        "heart": 0,
        "safe_choice": random.randint(0, 2),
        "heart_choice": random.randint(0, 2)
    })

# ================= 2. 🎨 스테이지별 동적 스타일 (배경색 변경 핵심) =================
def apply_style():
    # 4단계(반전)부터는 하얀 배경, 그 전에는 검정 배경
    if st.session_state.stage >= 4:
        bg_color = "white"
        text_color = "black"
        btn_border = "pink"
        btn_text = "red"
    else:
        bg_color = "black"
        text_color = "white"
        btn_border = "red"
        btn_text = "red"

    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: background-color 2s; /* 배경 바뀔 때 부드럽게 */
    }}
    button {{
        background-color: {bg_color} !important;
        color: {btn_text} !important;
        border: 2px solid {btn_border} !important;
    }}
    .center {{text-align:center;}}
    .big {{font-size:40px; font-weight:bold;}}
    .scary {{color:red; font-size:30px;}}
    .cute {{color:#ff4b4b; font-size:30px;}}
    </style>
    """, unsafe_allow_html=True)

apply_style()

# ================= 3. 🎧 음악 및 이미지 함수 =================
def play_audio(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', unsafe_allow_html=True)

def show_image(file_name):
    if os.path.exists(file_name):
        st.image(file_name, use_container_width=True)
    else:
        st.error(f"⚠️ {file_name} 파일을 찾을 수 없습니다. GitHub에 올렸는지 확인해주세요!")

# ================= 4. 게임 로직 =================

# --- 스테이지 0: 시작 ---
if st.session_state.stage == 0:
    st.markdown('<div class="center big">⚠️ 들어오면 안됐어</div>', unsafe_allow_html=True)
    if st.button("시작"):
        st.session_state.stage = 1
        st.session_state.bgm_started = True
        st.rerun()

# --- 스테이지 1: 공포 ---
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center scary">누가 보고 있어</div>', unsafe_allow_html=True)
    show_image("scary1.jpg")
    if st.button("계속"):
        st.session_state.stage = 2
        st.rerun()

# --- 스테이지 2: 생존 ---
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center big">살고 싶어? ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"문 {i+1}", key=f"s{i}"):
                if i == st.session_state.safe_choice:
                    st.session_state.survive += 1
                    st.toast("살았다...")
                else:
                    st.session_state.fail += 1
                    st.toast("틀렸어 🔪")
                st.session_state.safe_choice = random.randint(0, 2)
                st.rerun()

    if st.session_state.fail >= 3:
        st.error("나가는 게 쉽진 않지...")
        if st.button("다시 시도"):
            st.session_state.update({"stage": 0, "fail": 0, "survive": 0})
            st.rerun()
    if st.session_state.survive >= 3:
        if st.button("도망치기"):
            st.session_state.stage = 3
            st.rerun()

# --- 스테이지 3: 질문 ---
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center scary">정말 나를 믿어?</div>', unsafe_allow_html=True)
    if st.button("믿는다"):
        st.session_state.stage = 4
        st.rerun()
    if st.button("안 믿는다"):
        st.markdown('<div class="center big">💥 BOOM 💥</div>', unsafe_allow_html=True)

# --- 스테이지 4: 반전 (여기서 배경이 하얗게 변함) ---
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center cute">ㅋㅋ 놀랐지? 무서운 거 아니야!</div>', unsafe_allow_html=True)
    if st.button("...사실은"):
        st.session_state.bgm_type = "love"
        st.session_state.stage = 5
        st.rerun()

# --- 스테이지 5: 하트 모으기 ---
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center cute">하트 5개를 모아줘 💖 ({st.session_state.heart}/5)</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i == st.session_state.heart_choice:
                if st.button("💖", key=f"h{i}"):
                    st.session_state.heart += 1
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()
            else:
                if st.button("🖤", key=f"b{i}"):
                    st.toast("꽝!")
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()

    if st.session_state.heart >= 5:
        if st.button("다음으로"):
