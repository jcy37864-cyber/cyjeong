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
    "roulette_done": False, "dist": 100, "current_track": "", "last_result": ""
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
        background-color: {"#FFF0F0" if is_love else "#1A1A1A"} !important;
        color: {btn_c} !important; margin-bottom: 20px !important;
    }}
    .shake-text {{ display: inline-block; animation: shake 0.3s infinite; color: red; font-size: 35px; font-weight: bold; }}
    @keyframes shake {{ 0% {{transform: translate(2px, 2px);}} 50% {{transform: translate(-3px, -2px);}} 100% {{transform: translate(2px, 2px);}} }}
    .center {{ text-align: center; justify-content: center; }}
    .status-box {{ padding: 20px; border: 2px solid red; background: #111; color: white; border-radius: 10px; margin-bottom: 20px; font-size: 20px; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ================= 3. 🎵 오디오 함수 =================
def play_audio(file_name):
    if st.session_state.get("current_track") == file_name: return
    if os.path.exists(file_name):
        try:
            with open(file_name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            st.session_state.current_track = file_name
            audio_id = f"audio_{random.randint(0, 1000)}"
            st.markdown(f"""
                <audio id="{audio_id}" loop autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mpeg"></audio>
                <script>document.addEventListener('click', function() {{ document.getElementById('{audio_id}').play(); }}, {{ once: true }});</script>
            """, unsafe_allow_html=True)
        except: pass

def show_img(file_name):
    if os.path.exists(file_name): st.image(file_name, use_container_width=True)

# ================= 4. 메인 게임 로직 =================

if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ SYSTEM MALFUNCTION</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("🩸 권한 강제 탈취 (이소연)"):
            bar = st.progress(0); status_text = st.empty()
            msgs = ["접속 시도...", "보안 파괴...", "성공."]
            for i in range(101):
                time.sleep(0.03); bar.progress(i)
                status_text.markdown(f'<div class="center">{msgs[min(i//35, len(msgs)-1)]}</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True; st.rerun()
    else:
        st.error("⚠️ 접속 승인. 화면 클릭 시 소리가 들립니다.")
        if st.button("💀 어둠 속으로 입장"): st.session_state.stage = 1; st.rerun()

elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">🔪 소연아!! 뒤를 봐!! 🔪</div>', unsafe_allow_html=True)
    show_img("scary.jpg")
    st.markdown(f'<div class="center" style="font-size:25px;">거리: <b style="color:red;">{st.session_state.dist}m</b></div>', unsafe_allow_html=True)
    if st.session_state.dist > 0:
        if st.button("🏃 미친 듯이 질주하기!!"): st.session_state.dist -= 20; st.rerun()
    else:
        if st.button("🚪 다음 통로로 탈출"): st.session_state.stage = 2; st.rerun()

# --- [Stage 2] 문 선택 (수정 완료) ---
elif st.session_state.stage == 2:
    play_audio("bgm_scary.mp3")
    
    # 1. 성공 횟수 표시
    st.markdown(f'<div class="center" style="font-size:30px;">어느 문이 안전할까? 🚪 ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    
    # 2. 실패했을 때 (3회 이상)
    if st.session_state.fail >= 3:
        show_img("jumpscare.jpg")
        st.error("잡혔다... 놈이 네 뒤에 있어.")
        if st.button("🩸 영혼을 다시 꿰매고 재도전"):
            st.session_state.survive = 0; st.session_state.fail = 0; st.rerun()
    
    # 3. 3번 성공하기 전에는 문을 보여줌
    elif st.session_state.survive < 3:
        if random.random() > 0.7: show_img("scary2.jpg")
        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                if st.button(f"👁️ 문 {i+1}", key=f"door_{i}"):
                    if i == st.session_state.safe_choice: st.session_state.survive += 1
                    else: st.session_state.fail += 1
                    st.session_state.safe_choice = random.randint(0, 2); st.rerun()
    
    # 4. ★3번 성공 시 - 다른 것들 다 숨기고 탈출 버튼만 크게!★
    else:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.success("모든 문을 통과했어! 탈출구가 눈앞에 있다!")
        if st.button("🔦 황금빛 탈출구로 필사적으로 뛰기 🔦"):
            st.session_state.stage = 2.5; st.rerun()

# --- [Stage 2.5] 룰렛 (수정 완료) ---
elif st.session_state.stage == 2.5:
    play_audio("bgm_scary.mp3")
    st.markdown('<div class="center shake-text">💀 죽음의 룰렛 💀</div>', unsafe_allow_html=True)
    
    # 결과 메시지 고정 출력
    if st.session_state.last_result:
        st.markdown(f'<div class="status-box center">{st.session_state.last_result}</div>', unsafe_allow_html=True)
    
    # 룰렛 진행 중일 때
    if not st.session_state.roulette_done:
        if st.button("🎰 운명을 걸고 룰렛 돌리기 (2연속 성공 필요)"):
            with st.spinner("회전 중..."):
                time.sleep(1)
                if random.choice(["꽝", "통과", "꽝"]) == "통과":
                    st.session_state.roulette_score += 1
                    st.session_state.last_result = f"🎉
