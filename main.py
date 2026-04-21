import streamlit as st
import random
import os
import base64
import time

# ================= 1. 페이지 설정 =================
st.set_page_config(page_title="For Soyeon", page_icon="💖", layout="centered")

# 세션 상태 초기화
for key, val in {
    "stage": 0, "survive": 0, "fail": 0, "heart": 0,
    "safe_choice": random.randint(0, 2), "heart_choice": random.randint(0, 2),
    "loading_done": False, "trust_count": 0, "roulette_score": 0,
    "roulette_done": False, "dist": 100, "current_track": "", "last_result": "",
    "red_thread": random.randint(0, 4)
}.items():
    if key not in st.session_state: st.session_state[key] = val

# ================= 2. 🎨 디자인 테마 (HTML 스타일 이식) =================
def apply_theme():
    is_love = st.session_state.stage >= 4
    # HTML의 감성을 살린 부드러운 화이트/핑크 테마
    bg, txt, btn_c = ("#FFF9FA", "#4A4A4A", "#FF6B6B") if is_love else ("#000000", "#FF0000", "#8B0000")
    
    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; transition: all 1.2s ease-in-out; }}
    div.stButton > button {{
        width: 100% !important; height: 85px !important; font-size: 22px !important;
        font-weight: bold !important; border-radius: 20px !important;
        border: 3px solid {btn_c} !important;
        background-color: {"#FFFFFF" if is_love else "#111111"} !important;
        color: {btn_c} !important; margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .shake-text {{ display: inline-block; animation: shake 0.3s infinite; color: red; font-size: 38px; font-weight: bold; }}
    @keyframes shake {{ 0% {{transform: translate(3px, 3px);}} 50% {{transform: translate(-4px, -3px);}} 100% {{transform: translate(3px, 3px);}} }}
    .center {{ text-align: center; justify-content: center; }}
    /* HTML 편지 디자인 이식 */
    .letter-box {{ 
        background: white; padding: 50px; border-radius: 30px; 
        border: 1px solid #FFD1D1; color: #444; 
        box-shadow: 0px 20px 40px rgba(255, 182, 193, 0.4);
        font-family: 'Nanum Gothic', sans-serif;
    }}
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
    else: st.error(f"🖼️ [이미지 경로 확인] {file_name}")

# ================= 4. 메인 게임 로직 =================

# [Stage 0~5.5] 이전 공포 로직 및 하트 잡기는 그대로 유지됩니다 (코드 간소화 위해 생략하지만 실제 실행 시 포함됨)
# ... (앞부분 생략) ...
if st.session_state.stage == 0:
    st.markdown('<div class="center" style="font-size:35px; font-weight:bold;">👁️ SYSTEM BREACH</div>', unsafe_allow_html=True)
    if not st.session_state.loading_done:
        if st.button("🩸 권한 강제 탈취 (이소연)"):
            bar = st.progress(0); status_text = st.empty()
            for i in range(101):
                time.sleep(0.08); bar.progress(i)
                status_text.markdown(f'<div class="center">이소연님 데이터 복구 중... {i}%</div>', unsafe_allow_html=True)
            st.session_state.loading_done = True; st.rerun()
    else:
        if st.button("💀 어둠 속으로 입장"): st.session_state.stage = 1; st.rerun()

elif st.session_state.stage == 1:
    play_audio("bgm_scary.mp3"); show_img("scary.jpg")
    st.markdown('<div class="center shake-text">🔪 소연아!! 뒤를 봐!! 🔪</div>', unsafe_allow_html=True)
    if st.session_state.dist > 0:
        if st.button("🏃 질주하기!!"): st.session_state.dist -= 20; st.rerun()
    else:
        if st.button("🚪 탈출하기"): st.session_state.stage = 2; st.rerun()

# [중간 과정 생략 - 이전 답변의 2, 2.5, 3, 4, 5, 5.5 스테이지 로직이 들어가는 자리입니다]
# ... (생략된 부분은 위에서 제공한 코드와 동일하게 채우시면 됩니다) ...
elif st.session_state.stage == 2:
    st.markdown(f'<div class="center" style="font-size:30px;">어느 문이 안전할까? ({st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    if st.session_state.fail >= 3:
        show_img("jumpscare.jpg")
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
        if st.button("🔦 탈출구 발견!"): st.session_state.stage = 2.5; st.rerun()

elif st.session_state.stage == 2.5:
    if not st.session_state.roulette_done:
        if st.button("🎰 룰렛 돌리기"):
            if random.choice([True, False]): st.session_state.roulette_done = True
            else: show_img("jumpscare.jpg")
            st.rerun()
    else:
        if st.button("🩸 탈출"): st.session_state.stage = 3; st.rerun()

elif st.session_state.stage == 3:
    st.markdown('<div class="center" style="font-size:25px;">소연아, 나 믿어?</div>', unsafe_allow_html=True)
    if st.button("🔪 믿어..."): st.session_state.stage = 4; st.rerun()

elif st.session_state.stage == 4:
    play_audio("bgm_love.mp3"); show_img("cute.jpg"); st.balloons()
    if st.button("💖 진심 확인하기"): st.session_state.stage = 5; st.rerun()

elif st.session_state.stage == 5:
    st.markdown(f'<div class="center" style="font-size:30px;">하트 채우기 ({st.session_state.heart}/10)</div>', unsafe_allow_html=True)
    if st.button("💖"): 
        st.session_state.heart += 1
        if st.session_state.heart >= 10: st.session_state.stage = 5.5
        st.rerun()

elif st.session_state.stage == 5.5:
    st.markdown('<div class="center" style="font-size:30px;">🧶 운명의 실 고르기</div>', unsafe_allow_html=True)
    if st.button("🧶 우리의 실"): st.session_state.stage = 6; st.rerun()

# --- [Stage 6] HTML 고백 내용 이식 핵심부 ---
elif st.session_state.stage == 6:
    play_audio("bgm_love.mp3")
    # 아래 <div> 태그 안에 기존 HTML 파일의 주요 멘트를 넣으시면 됩니다.
    st.markdown(f"""
        <div class="letter-box">
            <h2 style="color: #FF6B6B; text-align: center; font-family: 'Nanum Pen Script', cursive;">소연이에게 전하는 진심</h2>
            <hr style="border: 0; border-top: 1px solid #FFD1D1; margin: 20px 0;">
            <p style="font-size: 19px; line-height: 2.0; text-align: center; color: #555;">
                여태까지 무서운 거 참느라 고생 많았어, 내 사랑 소연아.<br>
                사실 이 게임을 만든 건, 네가 어떤 상황에서도<br>
                내가 옆에 있다는 걸 보여주고 싶어서였어.<br><br>
                무서운 괴물도, 꽉 막힌 문도 우리가 함께라면 다 이겨냈듯이<br>
                앞으로의 우리 앞날도 지금처럼 같이 헤쳐나가고 싶어.<br><br>
                <b>이 세상에서 내가 가장 아끼고 사랑하는 소연아,</b><br>
            </p>
            <h1 style="text-align: center; color: #FF6B6B; margin-top: 30px; font-size: 40px;">나랑 평생 연애할래?</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌸 응! 좋아! 🌸"): 
            st.session_state.stage = 7; st.rerun()
    with col2:
        if st.button("좀 더 생각해볼래"): 
            st.warning("탈출구는 이미 폐쇄되었습니다! (선택지는 하나뿐이야 😊)")

# [Stage 7] 엔딩
elif st.session_state.stage == 7:
    play_audio("bgm_love.mp3"); st.balloons()
    show_img("final.jpg")
    st.markdown('<div class="center"><h1 style="color:#FF6B6B;">🌹 오늘부터 1일 🌹</h1><p style="font-size:20px;">내 곁에 와줘서 고마워. 사랑해 소연아!</p></div>', unsafe_allow_html=True)
    if st.button("처음으로"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
