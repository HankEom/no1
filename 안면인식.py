import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 설정 및 초기화 ---
st.set_page_config(
    page_title="FaceCheck EDU by SPARTA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'attendance_records' not in st.session_state:
    st.session_state.attendance_records = []
if 'attendance_triggered' not in st.session_state:
    st.session_state.attendance_triggered = False

# --- 사이드바 UI ---
st.sidebar.title("FaceCheck EDU")
st.sidebar.image("sparta_logo.png", use_column_width=True, caption="Powered by SPARTA") # 로고 삽입
st.sidebar.markdown("---")

st.sidebar.slider(
    "정시 출석 허용 시간 (분)", 1, 30, 5,
    help="실제 서비스에서 수업 시작 후 지정된 시간 이내에 출석을 완료해야 합니다."
)
st.sidebar.markdown("---")
st.sidebar.header("서비스 정보")
st.sidebar.info("""
    **FaceCheck EDU**는 온라인 학습 환경에서 대리 출석, 영상 도용 등 부정 출결을 방지하고, 
    학습자의 실시간 출석 상태 및 수업 참여 이력을 정확하게 기록합니다.
    관리자는 대시보시드를 통해 수강생 출석 신뢰도를 한눈에 파악할 수 있습니다.
""")


# --- 메인 페이지 제목 및 설명 ---
st.title("🎓 FaceCheck EDU: 온라인 교육 출결 관리 시스템")
st.markdown(f"""
    <p style="font-size:1.1em; color:#555;">
    AI 기술을 활용하여 온라인 교육 환경에서 부정 출결을 방지하고, 
    학습자의 실시간 출석 상태 및 수업 참여 이력을 정확하게 기록합니다.
    관리자는 대시보드를 통해 수강생 출석 신뢰도를 한눈에 파악할 수 있습니다.
    </p>
    <hr style="border:1px solid #eee;">
""", unsafe_allow_html=True)


# --- 출석 확인 섹션 ---
st.header("📝 출석 확인 시뮬레이션")
st.markdown("""
    <p style="font-size:0.95em; color:#777;">
    아래 '출석하기' 버튼을 클릭하여 출석 과정을 시뮬레이션합니다. 
    실제 서비스에서는 웹캠을 통해 얼굴이 인식되고 라이브니스 검증이 진행됩니다.
    </p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🖥️ 시연 화면")
    # ****** 이 부분을 수정합니다! ******
    # 웹캠 시뮬레이션 이미지 파일을 직접 참조
    st.image("webcam_simulation.png", 
             caption="웹캠 화면 시뮬레이션 (AI 얼굴 인식 동작 시연)", use_column_width=True)
    
    st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; border-left: 5px solid #e8344e; margin-top:20px;">
            <p style="font-size:1.1em; color:#e8344e; font-weight:bold;">현재 상태: 얼굴 감지 대기 중 (시뮬레이션)</p>
            <p style="font-size:0.9em; color:#555;">'출석하기' 버튼을 누르면 출석 시도가 시작됩니다.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("💡 출석 안내")
    st.info("""
        1. **얼굴 중앙 정렬**: (실제 서비스) 웹캠 화면에 얼굴을 중앙에 맞춰주세요.
        2. **라이브니스 검증**: (실제 서비스) 눈 깜빡임, 고개 움직임 등 생체 반응으로 실제 사람인지 확인합니다.
        3. **정시 출석**: (실제 서비스) 수업 시작 후 지정된 시간 이내에 출석을 완료해야 합니다.
    """)
    st.markdown("---")
    
    # 출석 버튼
    if st.button("🔴 출석하기", type="primary", use_container_width=True):
        st.session_state.attendance_triggered = True
        st.toast("출석 시도 중...", icon="⏳")
        time.sleep(2) # 출석 처리 시간 시뮬레이션
        
        # 시뮬레이션 결과
        status_options = ["출석 완료", "지각 처리", "부정 출석 감지"]
        simulated_status = np.random.choice(status_options, p=[0.7, 0.2, 0.1]) # 70% 출석, 20% 지각, 10% 부정

        new_record = {
            "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "학습자 ID": f"학생_{np.random.randint(100, 999)}",
            "상태": simulated_status,
            "감지된 얼굴 수": 1 if simulated_status != "부정 출석 감지" else np.random.randint(2,4), # 부정 시 여러 얼굴
            "라이브니스 검증": "통과" if simulated_status == "출석 완료" else "실패/N/A (시연용)"
        }
        st.session_state.attendance_records.insert(0, new_record) # 최신 기록을 상단에 추가

        if simulated_status == "출석 완료":
            st.success("✅ 출석이 성공적으로 완료되었습니다! (시뮬레이션)")
            st.toast("🎉 출석 완료!", icon="✅")
        elif simulated_status == "지각 처리":
            st.warning("⏰ 지각 처리되었습니다. (시뮬레이션)")
            st.toast("지각 처리!", icon="⏰")
        else:
            st.error("🚨 부정 출석이 감지되었습니다! (시뮬레이션)")
            st.toast("부정 출석 감지!", icon="🚨")
        
        st.session_state.attendance_triggered = False # 트리거 초기화


st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)

# --- 관리자 대시보드 섹션 ---
st.header("📊 관리자 대시보드 (출석 통계 및 기록)")
st.markdown(f"""
    <p style="font-size:0.95em; color:#777;">
    관리자는 아래 대시보드를 통해 수강생의 출석 현황과 부정 출석 시도를 한눈에 파악할 수 있습니다.
    <span style="color:#e8344e; font-weight:bold;">(시뮬레이션 데이터)</span>
    </p>
""", unsafe_allow_html=True)

if st.session_state.attendance_records:
    df_attendance = pd.DataFrame(st.session_state.attendance_records)
    
    # 상태별 색상 적용 (CSS 직접 주입)
    def highlight_status(s):
        if s['상태'] == '출석 완료':
            return ['background-color: #e6ffe6'] * len(s) # 연한 초록
        elif s['상태'] == '지각 처리':
            return ['background-color: #fffacd'] * len(s) # 레몬색
        elif s['상태'] == '부정 출석 감지':
            return ['background-color: #ffe6e6'] * len(s) # 연한 빨강
        return [''] * len(s)

    st.dataframe(df_attendance.style.apply(highlight_status, axis=1), use_container_width=True)
    
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("총 출석 시도", len(df_attendance))
    with col_stats2:
        successful_attendances = df_attendance[df_attendance['상태'] == '출석 완료'].shape[0]
        st.metric("성공적인 출석", successful_attendances, delta_color="normal")
    with col_stats3:
        fraud_attempts = df_attendance[df_attendance['상태'] == '부정 출석 감지'].shape[0]
        st.metric("부정 출석 감지", fraud_attempts, delta_color="inverse") # 부정은 역방향
        
    st.download_button(
        label="📥 출석 기록 다운로드 (CSV)",
        data=df_attendance.to_csv(index=False).encode('utf-8'),
        file_name="facecheck_edu_attendance_record.csv",
        mime="text/csv",
        help="현재 세션의 출석 기록을 CSV 파일로 다운로드합니다."
    )
else:
    st.info("아직 출석 기록이 없습니다. 상단의 '출석하기' 버튼을 눌러 시뮬레이션을 시작하세요.")

st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)

# --- 저작권 ---
st.markdown(f"<p style='text-align:center; color:#777; font-size:0.8em;'>© 2025 FaceCheck EDU. Powered by <span style='color:#e8344e; font-weight:bold;'>SPARTA</span>. All rights reserved.</p>", unsafe_allow_html=True)
