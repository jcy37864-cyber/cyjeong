import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 =================
st.set_page_config(page_title="scare", page_icon="💀", layout="centered")

# 세션 상태 초기화
for key, val in {
    "stage": 0, "survive": 0, "fail": 0, "heart": 0,
    "safe_choice": random.randint(0, 2), "heart_choice": random.randint(0, 2),
    "loading_done": False, "trust_count": 0, "roulette_score": 0,
    "roulette_done": False, "dist": 100, "current_track": "", "last_result": "",
    "red_thread": random.randint(0, 4) # 붉은 실 정답 번호
}.items():
    if key not in st.session_state: st.session_state[key] = val

# ================= 2. 🎨 디자인 테마 =================
def apply_theme():
    is_love = st.session_state.stage >= 4
    bg, txt, btn_c = ("#FFFFFF", "#333333", "#FF4B4B") if is_love else ("#000000", "#FF0000", "#8B0000")
    
    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; transition: all 0.5s ease; }}
    div.stButton > button {{
        width: 100% !important; height: 80px !important; font-size: 22px !important;
        font-weight: bold !important; border-radius: 15px !important;
        border: 3px solid {btn_c} !important;
        background-color: {"#FFF0F0" if is_love else "#111111"} !important;
        color: {btn_c} !important; margin-bottom: 15px !important;
    }}
    .shake-text {{ display: inline-block; animation: shake 0.3s infinite; color: red; font-size: 38px; font-weight: bold; }}
    @keyframes shake {{ 0% {{transform: translate(3px, 3px);}} 50% {{transform: translate(-4px, -3px);}} 100% {{transform: translate(3px, 3px);}} }}
    .center {{ text-align: center; justify-content: center; }}
    .status-box {{ padding: 20px; border: 3px solid red; background: #000; color: white; border-radius: 10px; margin-bottom: 20px; font-size: 22px; }}
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
            audio_id = f"audio_{int(time.time())}"
            st.markdown(f"""
                <audio id="{audio_id}" loop autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mpeg"></audio>
                <script>document.addEventListener('click', function() {{ document.getElementById('{audio_id}').play(); }}, {{ once: true }});</script>
            """, unsafe_allow_html=True)
        except: pass

def show_img(file_name):
    if os.path.exists(file_name): st.image(file_name, use_container_width=True)
    else: st.error(f"🖼️ [이미지 없음] {file_name}")

# ================= 4. 메인 게임 로직 =================

# [Stage 0~3] 기존 공포 로직 (생략 없이 유지)
if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ SYSTEM BREACH</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("🩸 권한 강제 탈취 (이소연)"):
            bar = st.progress(0); status_text = st.empty()
            for i in range(101):
                time.sleep(0.08); bar.progress(i) # 로딩시간 2배
                status_text.markdown(f'<div class="center">데이터 복구 중... {i}%</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True; st.rerun()
    else:
        if st.button("💀 어둠 속으로 입장"): st.session_state.stage = 1; st.rerun()

elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3"); show_img("scary.jpg")
    st.markdown('<div class="center shake-text">🔪 소연아!! 도망쳐!! 🔪</div>', unsafe_allow_html=True)
    if st.session_state.dist > 0:
        if st.button("🏃 질주하기!!"): st.session_state.dist -= 20; st.rerun()
    else:
        if st.button("🚪 다음 방으로"): st.session_state.stage = 2; st.rerun()

elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    st.markdown(f'<div class="center" style="font-size:30px;">어느 문이 안전할까? ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    if st.session_state.fail >= 3:
        show_img("jumpscare.jpg"); st.error("잡혔다.")
        if st.button("🩸 재도전"): st.session_state.survive = 0; st.session_state.fail = 0; st.rerun()
    elif st.session_state.survive < 3:
        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                if st.button(f"👁️ 문 {i+1}", key=f"door_{i}"):
                    if i == st.session_state.safe_choice: st.session_state.survive += 1
                    else: st.session_state.fail += 1
                    st.session_state.safe_choice = random.randint(0, 2); st.rerun()
    else:
        if st.button("🔦 탈출구로 뛰기 🔦"): st.session_state.stage = 2.5; st.rerun()

elif st.session_state.stage == 2.5:
    play_audio("bgm_scary.mp3")
    if st.session_state.last_result: st.markdown(f'<div class="status-box center">{st.session_state.last_result}</div>', unsafe_allow_html=True)
    if not st.session_state.roulette_done:
        if st.button("🎰 죽음의 룰렛 돌리기 (2연속)"):
            with st.spinner("운명 결정 중..."):
                time.sleep(1.2)
                if random.choice(["꽝", "통과", "꽝"]) == "통과":
                    st.session_state.roulette_score += 1
                    if st.session_state.roulette_score >= 2: st.session_state.roulette_done = True
                    st.session_state.last_result = "🎉 통과! 한 번 더!"
                else:
                    st.session_state.roulette_score = 0; st.session_state.last_result = "💀 [꽝]"; show_img("jumpscare.jpg")
            st.rerun()
    else:
        if st.button("🩸 틈새로 기어나가기"): st.session_state.stage = 3; st.rerun()

elif st.session_state.stage == 3:
    play_audio("bgm_scary.mp3"); show_img("scary.jpg")
    st.markdown('<div class="center" style="font-size:25px;">소연아, 나 믿어?</div>', unsafe_allow_html=True)
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
    play_audio("bgm_love.mp3"); st.balloons()
    st.markdown('<div class="center" style="font-size:35px; color:#FF4B4B;">🌹 놀랐지? 소연아! 🌹</div>', unsafe_allow_html=True)
    show_img("cute.jpg")
    if st.button("💖 진심을 확인할래?"): st.session_state.stage = 5; st.rerun()

# [Stage 5] 하트 잡기
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center" style="font-size:28px;">마음을 가득 채워줘! 💖 ({st.session_state.heart}/10)</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i == st.session_state.heart_choice:
                if st.button("💖", key=f"h_{i}"):
                    st.session_state.heart += 1
                    st.session_state.heart_choice = random.randint(0, 2); st.rerun()
            else:
                if st.button("🤍", key=f"e_{i}"): st.session_state.heart_choice = random.randint(0, 2); st.rerun()
    if st.session_state.heart >= 10:
        if st.button("✨ 운명의 실 선택하기 ✨"): st.session_state.stage = 5.5; st.rerun()

# --- [Stage 5.5] NEW! 운명의 붉은 실 선택 ---
elif st.session_state.stage == 5.5:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center" style="font-size:30px; color:#FF4B4B; font-weight:bold;">🧵 운명의 붉은 실 선택 🧵</div>', unsafe_allow_html=True)
    st.markdown('<div class="center">수많은 인연 중 우리의 실은 단 하나뿐이야.<br>소연아, 우리의 연결고리를 찾아줘.</div>', unsafe_allow_html=True)
    
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            if st.button("🧵", key=f"thread_{i}"):
                if i == st.session_state.red_thread:
                    st.session_state.stage = 6; st.rerun()
                else:
                    st.toast("이 실은 끊어져 있나 봐... 다시 골라줘!")
                    time.sleep(0.5)

# [Stage 6] 최종 고백
elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    st.markdown('<div class="center" style="font-size:32px; font-weight:bold;">소연아, 내 곁에 평생 있어줄래?</div>', unsafe_allow_html=True)
    if st.button("✨ 1000% YES! ✨"): st.session_state.stage = 7; st.rerun()

elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3"); st.balloons(); show_img("final.jpg")
    st.markdown('<div class="center" style="font-size:25px;">사랑해, 소연아! 💖</div>', unsafe_allow_html=True)
    if st.button("처음으로"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
