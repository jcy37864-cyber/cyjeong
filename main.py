import streamlit as st
import random
import os
import base64

# ================= 1. 페이지 설정 및 세션 상태 초기화 =================
st.set_page_config(page_title="scare", page_icon="🎨", layout="centered")

# 게임 데이터를 저장하는 '기억 저장소'
if "stage" not in st.session_state:
    st.session_state.update({
        "stage": 0,
        "survive": 0,
        "fail": 0,
        "heart": 0,
        "safe_choice": random.randint(0, 2),
        "heart_choice": random.randint(0, 2),
        "status_msg": ""
    })

# ================= 2. 🎨 분위기별 동적 스타일 (디자인 업그레이드) =================
def apply_theme():
    # 4단계(반전)부터는 핑크&화이트 테마, 그 전엔 호러 테마
    if st.session_state.stage >= 4:
        bg, text, accent, btn_bg = "#FFFFFF", "#333333", "#FF4B4B", "#FFF0F0"
    else:
        bg, text, accent, btn_bg = "#000000", "#FF0000", "#8B0000", "#1A1A1A"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; transition: all 1s ease; }}
    
    /* 버튼 스타일 통일 및 개선 */
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {accent} !important;
        border: 2px solid {accent} !important;
        border-radius: 15px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        transform: scale(1.05);
        background-color: {accent} !important;
        color: white !important;
    }}
    .center {{ text-align: center; }}
    .big-text {{ font-size: 40px; font-weight: bold; margin-bottom: 20px; }}
    .info-text {{ font-size: 20px; margin-bottom: 10px; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 🖼️ 미디어 처리 유틸리티 =================
def play_audio(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', unsafe_allow_html=True)

def show_img(file_name):
    if os.path.exists(file_name):
        st.image(file_name, use_container_width=True)
    else:
        st.caption(f"(이미지 {file_name}을 찾을 수 없습니다)")

# ================= 4. 게임 스테이지별 실행 로직 =================

# --- [0] 시작화면 ---
if st.session_state.stage == 0:
    st.markdown('<div class="center big-text">👁️ WARNING</div>', unsafe_allow_html=True)
    st.markdown('<div class="center info-text">게임을 좋아하는 이소연... 허락 없이 들어온 대가는 가혹할 거야../n(1부터 20까지 시간을 카운트후 입장.) </div>', unsafe_allow_html=True)
    if st.button("운명을 확인하기"):
        st.session_state.stage = 1
        st.rerun()

# --- [1] 공포의 서막 ---
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center big-text">누군가 널 지켜보고 있어......으악...</div>', unsafe_allow_html=True)
    show_img("scary.jpg")
    if st.button("도망치기 위해 계속 가기"):
        st.session_state.stage = 2
        st.rerun()

# --- [2] 생존 선택 게임 (문 고르기) ---
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center big-text">죽음의 선택.... ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    st.markdown('<div class="center info-text">단 하나의 문만 살아서 나갈 수 있다.</div>', unsafe_allow_html=True)
    
    # 깜짝 이미지 확률적 등장
    if random.random() > 0.8: show_img("jumpscare.jpg")
    
    # 버튼 레이아웃
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"문 {i+1}", key=f"door_{i}"):
                if i == st.session_state.safe_choice:
                    st.session_state.survive += 1
                    st.toast("...희망이보여...")
                else:
                    st.session_state.fail += 1
                    st.toast("크크큭... 틀렸어.....")
                st.session_state.safe_choice = random.randint(0, 2)
                st.rerun()

    # 결과 체크
    if st.session_state.fail >= 3:
        st.error("영원히 이곳에 갇혔습니다....")
        if st.button("다시 처음부터 도전"):
            st.session_state.clear()
            st.rerun()
    
    if st.session_state.survive >= 3:
        if st.button("희미한 빛이 보이는 곳으로 탈출"):
            st.session_state.stage = 3
            st.rerun()

# --- [3] 마지막 심리전 ---
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center big-text">자 이제 마지막 질문이다...</div>', unsafe_allow_html=True)
    show_img("scary2.jpg")
    st.markdown('<div class="center info-text" style="color:red;">너는, 나를 믿어?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("믿는다"):
            st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("절대 못 믿어"):
            st.markdown('<h1 class="center">💥 공격 당했습니다 💥</h1>', unsafe_allow_html=True)
            if st.button("부활하기"):
                st.session_state.clear()
                st.rerun()

# --- [4] 반전 (배경 화이트 전환) ---
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center big-text" style="color:#FF4B4B;">🎉 Surprise! 🎉</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    st.markdown('<div class="center info-text">무서웠지? 사실 널 위해 준비한 작은 이벤트야!</div>', unsafe_allow_html=True)
    if st.button("진심을 확인해볼래?"):
        st.session_state.stage = 5
        st.rerun()

# --- [5] 하트 잡기 게임 (하트 카운트 최적화) ---
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center big-text" style="color:#FF4B4B;">내 마음을 잡아줘 💖</div>', unsafe_allow_html=True)
    st.progress(st.session_state.heart / 5) # 진행 바 추가
    st.markdown(f'<div class="center info-text">수집된 하트: {st.session_state.heart} / 5</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            # 하트 위치에 따른 버튼 설정
            if i == st.session_state.heart_choice:
                if st.button("💖", key=f"heart_btn_{i}"):
                    st.session_state.heart += 1
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()
            else:
                if st.button("🤍", key=f"empty_btn_{i}"):
                    st.toast("여긴 비었어!")
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()

    # 5개 모으면 즉시 다음 버튼 등장
    if st.session_state.heart >= 5:
        st.markdown("---")
        if st.button("모든 마음을 모았어! 클릭! ✨"):
            st.session_state.stage = 6
            st.rerun()

# --- [6] 최종 고백 ---
elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center big-text">사실은 말이야...</div>', unsafe_allow_html=True)
    st.markdown('<div class="center info-text" style="font-size:30px;"> 소연씨 나와 축복 받고, 영원히 함께 해주지 않을래? 🌹</div>', unsafe_allow_html=True)
    if st.button("YES! 나도 좋아 💖"):
        st.session_state.stage = 7
        st.rerun()

# --- [7] 엔딩 (QR코드 및 메시지) ---
elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3")
    st.balloons()
    st.markdown('<div class="center big-text" style="color:#FF4B4B;">우리 사랑 영원히 💖</div>', unsafe_allow_html=True)
    show_img("final.jpg")
    st.markdown('<div class="center info-text">위의 사진(QR)을 확인해봐!</div>', unsafe_allow_html=True)
    
    if st.button("처음으로 (다시 하기)"):
        st.session_state.clear()
        st.rerun()
