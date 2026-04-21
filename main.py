# --- [Stage 5] 하트 잡기 ---
elif st.session_state.stage == 5:
    play_audio("bgm_love.mp3")
    st.markdown(f'<div class="center big-text" style="color:#FF4B4B;">내 마음을 받아줘 💖 ({st.session_state.heart}/5)</div>', unsafe_allow_html=True)
    
    # 162번 줄 근처: 괄호와 들여쓰기 확인
    st.progress(st.session_state.heart / 5)
    
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i == st.session_state.heart_choice:
                if st.button("💖", key=f"h_btn_{i}"):
                    st.session_state.heart += 1
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()
            else:
                if st.button("🤍", key=f"e_btn_{i}"):
                    st.toast("다시 찾아봐!")
                    st.session_state.heart_choice = random.randint(0, 2)
                    st.rerun()

    # 하트 5개를 다 모았을 때 처리
    if st.session_state.heart >= 5:
        st.markdown("---")
        if st.button("모든 마음을 다 모았어! 클릭! ✨"):
            with st.spinner("마지막 진심을 전하기 위해 용기를 내는 중..."):
                time.sleep(5)
            st.session_state.stage = 6
            st.rerun()
