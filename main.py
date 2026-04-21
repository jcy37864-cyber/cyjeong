import streamlit as st
import random
import os

# ================= 1. 기본 설정 =================
st.set_page_config(page_title="익명의 메시지", page_icon="👁️", layout="centered")

# 세션 상태 초기화 (게임 데이터 보관함)
if "stage" not in st.session_state:
    st.session_state.update({
        "stage": 0,
        "bgm_started": False,
        "bgm_type": "scary",
        "survive": 0,
        "fail": 0,
        "heart": 0,
        "safe_choice": random.randint(0, 2), # 랜덤 정답 고정
        "heart_choice": random.randint(0, 2),
        "message": ""
    })

# ================= 2. 🎧 음악 재생 함수 =================
def play_bgm():
    if st.session_state.bgm_started:
        # 파일 경로가 실제 GitHub에 있는지 확인 필수
        file_path = "bgm_scary.mp3" if st.session_state.bgm_type == "scary" else "bgm_love.mp3"
        
        # Streamlit Cloud에서 오디오를 강제 재생하는 HTML
        audio_html = f"""
            <audio autoplay loop key="{st.session_state.bgm_type}">
                <source src="https://raw.githubusercontent.com/사용자계정/저장소명/main/{file_path}" type="audio/mp3">
            </audio>
            """
        # 로컬 파일 테스트용 (배포 시 위 URL 방식으로 교체 가능)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                data = f.read()
                import base64
                b64 = base64.b64encode(data).decode()
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay loop></audio>', unsafe_allow_html=True)

# ================= 3. 🎨 스타일 설정 =================
st.markdown("""
<style>
.stApp { background-color: black; color: white; }
button { background-color: black !important; color: red !important; border: 1px solid red !important; width: 100%; }
.center { text-align:center; }
.big { font-size:40px; font-weight: bold; }
.scary { color:red; font-size:30px; }
.cute { color:pink; font-size:30px; }
</style>
""", unsafe_allow_html=True)

# ================= 4. 게임 스테이지 로직 =================

# --- STAGE 0: 시작 ---
if st.session_state.stage == 0:
    st.markdown('<div class="center big">⚠️ 들어오면 안됐어</div>', unsafe_allow_html=True)
    if st.button("시작"):
        st.session_state.stage = 1
        st.session_state.bgm_started = True
        st.rerun()

# --- STAGE 1: 경고 ---
elif st.session_state.stage == 1:
    play_bgm()
    st.markdown('<div class="center scary">누가 보고 있어...</div>', unsafe_allow_html=True)
    if os.path.exists("scary1.jpg"):
        st.image("scary1.jpg", use_container_width=True)
    else:
        st.warning("이미지 파일(scary1.jpg)을 찾을 수 없습니다.")
        
    if st.button("계속"):
        st.session_state.stage = 2
        st.rerun()

# --- STAGE 2: 생존 게임 ---
elif st.session_state.stage == 2:
    play_bgm()
    st.markdown(f'<div class="center big">살고 싶어? (성공: {st.session_state.survive}/3)</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"문 {i+1}", key=f"s{i}"):
                if i == st.session_state.safe_choice:
                    st.session_state.survive += 1
                    st.session_state.message = "살았다..."
                else:
                    st.session_state.fail += 1
                    st.session_state.message = "틀렸어 🔪"
                # 정답 위치 재설정
                st.session_state.safe_choice = random.randint(0, 2)
                st.rerun()
    
    if st.session_state.message:
        st.write(f'<div class="center">{st.session_state.message}</div>', unsafe_allow_html=True)

    if st.session_state.fail >= 3:
        st.error("나가는게 쉽진 않지 하하하")
        if st.button("다시 처음부터"):
            st.session_state.update({"stage": 0, "fail": 0, "survive": 0})
            st.rerun()

    if st.session_state.survive >= 3:
        if st.button("도망치기"):
            st.session_state.stage = 3
            st.session_state.message = ""
            st.rerun()

# --- STAGE 3: 신뢰 ---
elif st.session_state.stage == 3:
    play_bgm()
    st.markdown('<div class="center scary">정말 나를 믿어?</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("믿는다"):
            st.session_state.stage = 4
            st.rerun()
    with col2:
        if st.button("안 믿는다"):
            st.error("💥 BOOM 💥")
            if st.button("되살아나기"):
                st.session_state.stage = 0
                st.rerun()

# --- STAGE 4: 반전 ---
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown('<div class="center cute">ㅋㅋ 놀랐지? 무서운 거 아니야!</div>', unsafe_allow_html=True)
    if st.button("...사실은"):
        st.session_state.bgm_type = "love"
        st.session_state.stage = 5
        st.rerun()

# --- STAGE 5: 하트 모으기 ---
elif st.session_state.stage == 5:
    play_bgm()
    st.markdown(f'<div class="center cute">하트 5개를 모아줘! 💖 ({st.session_state.heart}/5)</div>', unsafe_allow_html=True)
    
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
        if st.button("내 마음 확인하기"):
            st.session_state.stage = 6
            st.rerun()

# --- STAGE 6 & 7: 고백 ---
elif st.session_state.stage == 6:
    st.markdown('<div class="center big">사실은...</div>', unsafe_allow_html=True)
    if st.button("두근두근..."):
        st.session_state.stage = 7
        st.rerun()

elif st.session_state.stage == 7:
    st.markdown('<div class="center big">나랑 계속 함께해줄래? 🌹</div>', unsafe_allow_html=True)
    if st.button("YES 💖"):
        st.balloons()
        if os.path.exists("qr.png"):
            st.image("qr.png")
        else:
            st.success("내 마음이 너에게 전달되었어! (QR 코드를 추가해봐!)")
    if st.button("NO 😢"):
        st.warning("내 마음을 다시 한 번만 생각해줘...")
