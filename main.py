import streamlit as st
import random
import os
import base64

# ================= 1. 페이지 기본 설정 =================
st.set_page_config(page_title="???", page_icon="👁️", layout="centered")

# 세션 상태 초기화 (데이터 보존)
if "stage" not in st.session_state:
    st.session_state.update({
        "stage": 0,
        "bgm_type": "scary",
        "survive": 0,
        "fail": 0,
        "heart": 0,
        "safe_choice": random.randint(0, 2),
        "heart_choice": random.randint(0, 2),
        "flicker": False  # 전환 효과용
    })

# ================= 2. 유틸리티 함수 (이미지, 오디오) =================

def get_base64(file_path):
    """파일을 base64로 변환하여 브라우저에서 직접 재생/표시 가능하게 함"""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def play_audio(file_name):
    """오디오 자동 재생 (브라우저 정책상 첫 클릭 이후 작동)"""
    b64 = get_base64(file_name)
    if b64:
        st.markdown(f"""
            <audio autoplay loop>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

# ================= 3. 🎨 동적 스타일링 (아이디어 추가) =================
def apply_custom_style():
    # 스테이지에 따른 테마 색상 설정
    if st.session_state.stage >= 4:
        bg_color, text_color, accent = "#FFFFFF", "#333333", "#FF4B4B"
        font_family = "'Nanum Pen Script', cursive"
    else:
        bg_color, text_color, accent = "#0E1117", "#FF0000", "#8B0000"
        font_family = "serif"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap');
    
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: all 1.5s ease-in-out;
    }}
    
    /* 공포 분위기 글리치 효과 */
    .glitch {{
        font-size: 40px;
        font-weight: bold;
        text-transform: uppercase;
        position: relative;
        text-shadow: 0.05em 0 0 rgba(255,0,0,.75), -0.025em -0.05em 0 rgba(0,255,0,.75), 0.025em 0.05em 0 rgba(0,0,255,.75);
        animation: glitch 500ms infinite;
    }}
    
    @keyframes glitch {{
        0% {{ text-shadow: 1px 0 0 red, -1px 0 0 blue; }}
        50% {{ text-shadow: -1px 0 0 red, 1px 0 0 blue; }}
        100% {{ text-shadow: 1px 0 0 red, -1px 0 0 blue; }}
    }}

    /* 버튼 스타일 */
    button {{
        background-color: {bg_color} !important;
        color: {accent} !important;
        border: 1px solid {accent} !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        width: 100%;
    }}
    
    .center {{ text-align: center; font-family: {font_family}; }}
    </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# ================= 4. 게임 스테이지 로직 =================

# --- STAGE 0: 시작 ---
if st.session_state.stage == 0:
    st.markdown('<div class="center glitch">⚠️ WARNING ⚠️</div>', unsafe_allow_html=True)
    st.markdown('<p class="center">이 페이지는 위험한 내용을 포함할 수 있습니다.</p>', unsafe_allow_html=True)
    if st.button("진입하기"):
        st.session_state.stage = 1
        st.rerun()

# --- STAGE 1: 분위기 고조 ---
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center glitch">누가 보고 있어...</div>', unsafe_allow_html=True)
    
    img_b64 = get_base64("scary1.jpg")
    if img_b64:
        st.markdown(f'<div class="center"><img src="data:image/jpeg;base64,{img_b64}" width="100%"></div>', unsafe_allow_html=True)
    else:
        st.info("(공포스러운 그림자가 드리웁니다...)") # 파일 없을 때 대비

    if st.button("계속"):
        st.session_state.stage = 2
        st.rerun()

# --- STAGE 2: 생존 선택 ---
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">살고 싶어? ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"???", key=f"btn_{i}"):
                if i == st.session_state.safe_choice:
                    st.session_state.survive += 1
                    st.toast("...운이 좋군")
                else:
                    st.session_state.fail += 1
                    st.toast("틀렸어.")
                st.session_state.safe_choice = random.randint(0, 2)
                st.rerun()

    if st.session_state.fail >= 3:
        st.error("영원히 나갈 수 없습니다.")
        if st.button("다시 시도... 하시겠습니까?"):
            st.session_state.update({"stage":0, "fail":0, "survive":0})
            st.rerun()

    if st.session_state.survive >= 3:
        if st.button("빛이 보이는 곳으로"):
            st.session_state.stage = 3
            st.rerun()

# --- STAGE 3: 최종 관문 ---
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center glitch">마지막으로 묻지... 나를 믿어?</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("믿는다"):
            st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("믿지 않는다"):
            st.markdown('<div class="center" style="color:red; font-size:50px;">GAME OVER</div>', unsafe_allow_html=True)

# --- STAGE 4: 반전 (흰색 배경 전환) ---
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center" style="font-size:40px; color:#FF4B4B; font-family:\'Nanum Pen Script\';">짜잔! 놀랐지? 무서운 거 아니야! 🎁</div>', unsafe_allow_html=True)
    st.markdown('<p class="center" style="color:gray;">사실 널 위해 준비한 작은 서프라이즈야.</p>', unsafe_allow_html=True)
    if st.button("사실은..."):
        st.session_state.stage = 5
        st.rerun()

# --- STAGE 5: 하트 게임 (밝은 분위기) ---
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center" style="font-size:35px; color:#FF4B4B;">내 마음을 받아줘! 💖 ({st.session_state.heart}/5)</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i == st.session_state.heart_choice:
                if st.button("💖", key=f"heart_{i}"):
                    st.session_state.heart += 1
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()
            else:
                if st.button("🤍", key=f"empty_{i}"):
                    st.toast("다시 찾아봐!")
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()

    if st.session_state.heart >= 5:
        if st.button("확인하러 가기"):
            st.session_state.stage = 6
            st.rerun()

# --- STAGE 6: 최종 메시지 ---
elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center" style="font-size:40px;">나랑 계속...</div>', unsafe_allow_html=True)
    if st.button("함께해줄래?"):
        st.session_state.stage = 7
        st.rerun()

# --- STAGE 7: 결말 (QR 코드) ---
elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center" style="font-size:45px; color:#FF4B4B;">YES! 💖✨</div>', unsafe_allow_html=True)
    st.balloons()
    
    qr_b64 = get_base64("qr.png")
    if qr_b64:
        st.markdown(f'<div class="center"><img src="data:image/png;base64,{qr_b64}" width="250px"></div>', unsafe_allow_html=True)
    else:
        st.success("너를 위한 선물이 준비되어 있어! (qr.png 파일을 확인해줘)")
        
    if st.button("처음으로 돌아가기"):
        st.session_state.clear()
        st.rerun()
