import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 =================
st.set_page_config(page_title="scare", page_icon="💀", layout="centered")

if "stage" not in st.session_state: st.session_state.stage = 0
if "survive" not in st.session_state: st.session_state.survive = 0
if "fail" not in st.session_state: st.session_state.fail = 0
if "heart" not in st.session_state: st.session_state.heart = 0
if "safe_choice" not in st.session_state: st.session_state.safe_choice = random.randint(0, 2)
if "heart_choice" not in st.session_state: st.session_state.heart_choice = random.randint(0, 2)
if "loading_done" not in st.session_state: st.session_state.loading_done = False
if "trust_count" not in st.session_state: st.session_state.trust_count = 0
if "roulette_score" not in st.session_state: st.session_state.roulette_score = 0
if "roulette_done" not in st.session_state: st.session_state.roulette_done = False
if "dist" not in st.session_state: st.session_state.dist = 100
if "current_track" not in st.session_state: st.session_state.current_track = ""
if "last_result" not in st.session_state: st.session_state.last_result = "" # 룰렛 결과 유지용

# ================= 2. 🎨 디자인 테마 (버튼 크기 강화) =================
def apply_theme():
    is_love = st.session_state.stage >= 4
    bg = "#FFFFFF" if is_love else "#000000"
    txt = "#333333" if is_love else "#FF0000"
    btn_color = "#FF4B4B" if is_love else "#8B0000"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; transition: all 0.5s ease; }}
    /* 모든 버튼 공통 스타일 강화 */
    div.stButton > button {{
        width: 100% !important;
        height: 80px !important; /* 버튼 높이 증가 */
        font-size: 22px !important; /* 글씨 크기 증가 */
        font-weight: bold !important;
        border-radius: 15px !important;
        border: 3px solid {btn_color} !important;
        background-color: {"#FFF0F0" if is_love else "#1A1A1A"} !important;
        color: {btn_color} !important;
        margin-bottom: 20px !important;
    }}
    .shake-text {{ display: inline-block; animation: shake 0.3s infinite; color: red; font-size: 35px; font-weight: bold; }}
    @keyframes shake {{
        0% {{ transform: translate(2px, 2px); }}
        50% {{ transform: translate(-3px, -2px); }}
        100% {{ transform: translate(2px, 2px); }}
    }}
    .center {{ text-align: center; justify-content: center; }}
    .status-box {{ padding: 20px; border: 2px solid red; background: #111; color: white; border-radius: 10px; margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 기능 함수 =================
def play_audio(file_name):
    if st.session_state.get("current_track") == file_name: return
    if os.path.exists(file_name):
        try:
            with open(file_name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            st.session_state.current_track = file_name
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', unsafe_allow_html=True)
        except: pass

def show_img(file_name):
    if os.path.exists(file_name): st.image(file_name, use_container_width=True)

# ================= 4. 메인 로직 =================

# [Stage 0] 로딩
if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ SYSTEM MALFUNCTION</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("🩸 권한 강제 탈취 (이소연)"):
            bar = st.progress(0)
            status_text = st.empty()
            msgs = ["영혼 분석 중...", "금기된 구역 침입...", "보안 파쇄...", "접속됨."]
            for i in range(101):
                time.sleep(0.04)
                bar.progress(i)
                idx = min(i // 25, len(msgs)-1)
                status_text.markdown(f'<div class="center">{msgs[idx]}</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True
            st.rerun()
    else:
        st.error("⚠️ 이소연의 생존 신호가 확인되었습니다.")
        if st.button("💀 어둠 속으로 강제 입장"):
            st.session_state.stage = 1
            st.rerun()

# [Stage 1] 도망쳐!
elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">🔪 소연아!! 뒤를 봐!! 🔪</div>', unsafe_allow_html=True)
    show_img("scary.jpg")
    st.markdown(f'<div class="center" style="font-size:25px;">놈과의 거리: <b style="color:red;">{st.session_state.dist}m</b></div>', unsafe_allow_html=True)
    if st.session_state.dist > 0:
        if st.button("🏃 미친 듯이 질주하기!!"):
            st.session_state.dist -= 20
            st.rerun()
    else:
        st.success("거의 다 따돌렸어...!")
        if st.button("🚪 다음 통로로 필사적으로 이동"):
            st.session_state.stage = 2
            st.rerun()

# [Stage 2] 문 선택
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">어느 쪽이 삶의 문인가? ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"👁️ 문 {i+1}", key=f"door_{i}"):
                if i == st.session_state.safe_choice: st.session_state.survive += 1
                else: st.session_state.fail += 1
                st.session_state.safe_choice = random.randint(0, 2)
                st.rerun()
    
    if st.session_state.fail >= 3:
        show_img("jumpscare.jpg")
        if st.button("🩸 영혼을 다시 꿰매고 도전"):
            st.session_state.survive = 0; st.session_state.fail = 0; st.rerun()
    elif st.session_state.survive >= 3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # 잘 보이게 중앙 정렬된 거대 버튼
        if st.button("🔦 탈출구 발견! 살아나가기 🔦"):
            st.session_state.stage = 2.5
            st.rerun()

# [Stage 2.5] 공포의 룰렛 (강화)
elif st.session_state.stage == 2.5:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">💀 죽음의 룰렛 💀</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="center" style="font-size:20px;">연속 2번 "통과"가 나와야 살 수 있다... ({st.session_state.roulette_score}/2)</div>', unsafe_allow_html=True)
    
    # 결과가 유지되도록 빈 공간 활용
    res_box = st.empty()
    if st.session_state.last_result:
        res_box.markdown(f'<div class="status-box center">{st.session_state.last_result}</div>', unsafe_allow_html=True)

    if not st.session_state.roulette_done:
        if st.button("🎰 운명의 룰렛 돌리기 🎰"):
            with st.spinner("운명이 결정되는 중..."):
                time.sleep(1.2)
                if random.choice(["꽝", "통과", "꽝"]) == "통과":
                    st.session_state.roulette_score += 1
                    st.session_state.last_result = f"🎉 {st.session_state.roulette_score}회 성공! 살고 싶으면 한 번 더!"
                    if st.session_state.roulette_score >= 2: 
                        st.session_state.roulette_done = True
                        st.session_state.last_result = "🔓 봉인이 해제되었다!! 어서 나가!"
                else:
                    st.session_state.roulette_score = 0
                    st.session_state.last_result = "💀 [꽝] 놈이 네 발을 잡았어! 처음부터 다시!"
                    show_img("jumpscare.jpg")
            st.rerun()
    else:
        if st.button("🩸 열린 문으로 기어나가기"):
            st.session_state.stage = 3
            st.rerun()

# [Stage 3] 믿음 테스트
elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center" style="font-size:25px;">마지막 문턱이야. 소연아, 날 믿니?</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔪 믿어..."):
            st.session_state.trust_count += 1
            if st.session_state.trust_count >= 3: st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("🕯️ 못 믿겠어"): st.rerun()

# [Stage 4] 반전 고백
elif st.session_state.stage == 4:
    play_audio("bgm_love.mp3")
    st.balloons()
    st.markdown('<div class="center" style="font-size:35px; color:#FF4B4B;">🌹 서프라이즈! 소연아! 🌹</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    if st.button("💝 내 진심을 확인할래?"): 
        st.session_state.stage = 5
        st.rerun()

# [Stage 5] 하트 잡기 (10개)
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">마음을 가득 채워줘! 💖 ({st.session_state.heart}/10)</div>', unsafe_allow_html=True)
    st.progress(st.session_state.heart / 10)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i == st.session_state.heart_choice:
                if st.button("💖", key=f"h_{i}"):
                    st.session_state.heart += 1
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()
            else:
                if st.button("🤍", key=f"e_{i}"): st.session_state.heart_choice = random.randint(0, 2); st.rerun()
    
    if st.session_state.heart >= 10:
        if st.button("🌹 이제 모든 준비가 끝났어!"): 
            st.session_state.stage = 6
            st.rerun()

# [Stage 6~7] 최종 엔
