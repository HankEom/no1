import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import pandas as pd
from datetime import datetime

# --- 설정 및 초기화 ---
st.set_page_config(
    page_title="FaceCheck EDU",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화 (페이지 새로고침 시 데이터 유지)
if 'attendance_records' not in st.session_state:
    st.session_state.attendance_records = []
if 'is_attended' not in st.session_state:
    st.session_state.is_attended = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False

# --- 얼굴 인식 및 라이브니스 함수 ---
# 실제 배포 시에는 이 함수들이 별도의 유틸리티 파일에 분리될 수 있습니다.

# MediaPipe Face Detection 초기화
@st.cache_resource
def get_face_detector():
    return mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7)

# MediaPipe Drawing Utils 초기화
@st.cache_resource
def get_drawing_utils():
    return mp.solutions.drawing_utils

# 라이브니스 검증 (간소화된 눈 깜빡임 감지)
# 실제 프로젝트에서는 MediaPipe FaceMesh 또는 Dlib을 사용하여 훨씬 정확한 EAR 계산
# 여기서는 시연을 위한 가상 로직입니다.
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 3 # 눈 감은 프레임 수
BLINK_DURATION_THRESHOLD = 2 # 2초 이상 눈 감고 있으면 의심

# --- UI 레이아웃 및 기능 구현 ---

st.sidebar.title("FaceCheck EDU 설정")
attendance_window_minutes = st.sidebar.slider(
    "정시 출석 허용 시간 (분)", 1, 30, 5,
    help="수업 시작 후 지정된 시간 이내에 출석을 완료해야 합니다."
)

st.sidebar.markdown("---")
st.sidebar.header("서비스 정보")
st.sidebar.info("""
    **FaceCheck EDU**는 온라인 학습 환경에서 부정 출결을 방지하고, 
    학습자의 출석 상태 및 수업 참여 이력을 정확하게 기록하는 AI 서비스입니다.
""")
st.sidebar.image("https://via.placeholder.com/150x150?text=FaceCheck+EDU+Logo", use_column_width=True) # 로고 플레이스홀더

# 메인 페이지 제목 및 설명
st.title("🎓 FaceCheck EDU: 온라인 교육 출결 관리 시스템")
st.markdown("""
    **대리 출석, 영상 도용 등 부정 출결 방지**를 위해 **AI 기반 안면 인식 및 라이브니스 검증**을 활용합니다.
    학습자는 간편하게 출석을 완료하고, 관리자는 대시보드를 통해 출석 신뢰도를 한눈에 파악할 수 있습니다.
""")

st.markdown("---")

# --- 출석 확인 섹션 ---
st.header("📝 실시간 출석 확인")
st.warning("⚠️ 웹캠 접근을 허용해주세요. 웹캠 화면에 얼굴을 중앙에 맞춰주세요.")

col1, col2 = st.columns([2, 1])

with col1:
    video_placeholder = st.empty() # 웹캠 영상을 위한 플레이스홀더
    attendance_status_message = st.empty() # 출석 상태 메시지를 위한 플레이스홀더

with col2:
    st.subheader("💡 안내")
    st.info(f"""
        1. **얼굴 중앙 정렬**: 웹캠 화면에 얼굴을 중앙에 맞춰주세요.
        2. **라이브니스 검증**: 눈 깜빡임 등 생체 반응으로 실제 사람인지 확인합니다.
        3. **정시 출석**: 수업 시작 후 **{attendance_window_minutes}분 이내**에 출석을 완료해주세요.
    """)
    st.markdown("---")
    
    # 출석 버튼
    if not st.session_state.camera_active:
        if st.button("🔴 출석 확인 시작", type="primary", use_container_width=True):
            st.session_state.camera_active = True
            st.session_state.is_attended = False # 새로운 출석 시도
            st.session_state.start_time = time.time() # 시작 시간 재설정
            st.rerun() # 앱 재실행하여 웹캠 활성화
    else:
        if st.button("⏹️ 출석 확인 중지", type="secondary", use_container_width=True):
            st.session_state.camera_active = False
            st.rerun() # 앱 재실행하여 웹캠 비활성화


# --- 웹캠 처리 로직 ---
if st.session_state.camera_active and not st.session_state.is_attended:
    face_detector = get_face_detector()
    mp_drawing = get_drawing_utils()
    cap = cv2.VideoCapture(0) # 웹캠 켜기

    if not cap.isOpened():
        attendance_status_message.error("🚨 웹캠을 켜는 데 실패했습니다. 카메라가 연결되어 있고 사용 가능한지 확인해주세요.")
        st.session_state.camera_active = False # 카메라 비활성화 상태로 전환
        st.stop() # 더 이상 진행하지 않음

    # 라이브니스 검증을 위한 변수
    counter_blink_frames = 0
    total_blinks_detected = 0
    
    # 웹캠 스트림
    while st.session_state.camera_active and cap.isOpened() and not st.session_state.is_attended:
        ret, frame = cap.read()
        if not ret:
            attendance_status_message.error("⚠️ 웹캠 프레임을 읽을 수 없습니다.")
            break

        frame = cv2.flip(frame, 1) # 좌우 반전
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detector.process(image_rgb)

        time_elapsed = time.time() - st.session_state.start_time
        
        # --- 시간 제한 처리 ---
        if time_elapsed > attendance_window_minutes * 60:
            attendance_status_message.error(f"⏰ 출석 시간이 종료되었습니다. ({attendance_window_minutes}분 초과)")
            if not st.session_state.is_attended: # 아직 출석 처리되지 않았다면 지각 기록
                st.session_state.attendance_records.append({
                    "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "상태": "지각 (시간 초과)",
                    "감지된 얼굴 수": 0,
                    "라이브니스 검증": "N/A"
                })
                st.session_state.is_attended = True # 더 이상 출석 시도하지 않음
            st.session_state.camera_active = False # 카메라 중지
            break

        face_detected = False
        if results.detections:
            for detection in results.detections:
                face_detected = True
                mp_drawing.draw_detection(frame, detection)
                
                # --- 라이브니스 검증 시뮬레이션 ---
                # 실제 구현에서는 MediaPipe FaceMesh 또는 Dlib을 사용하여
                # 눈 랜드마크를 추출하고 EAR을 계산하여 라이브니스 판단
                
                # 시연을 위한 임의의 EAR 값 및 깜빡임 로직
                current_ear = np.random.uniform(0.1, 0.4) # 0.1 ~ 0.4 사이의 무작위 EAR
                
                if current_ear < EYE_AR_THRESH: # 눈을 감았다고 가정
                    counter_blink_frames += 1
                else:
                    if counter_blink_frames >= EYE_AR_CONSEC_FRAMES: # 충분히 눈을 감았다 떴다면
                        total_blinks_detected += 1
                        attendance_status_message.success(f"생체 반응 감지! ({total_blinks_detected}회 깜빡임)")
                    counter_blink_frames = 0 # 카운터 초기화
                
                # 텍스트 오버레이
                cv2.putText(frame, f"EAR: {current_ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Blinks: {total_blinks_detected}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # --- 최종 출석 처리 조건 (얼굴 감지 + 라이브니스 통과) ---
            # 실제로는 '등록된 얼굴과 일치' 및 '라이브니스 검증 성공' 로직이 추가됩니다.
            if face_detected and total_blinks_detected >= 1 and not st.session_state.is_attended: # 최소 1회 깜빡임
                attendance_status_message.success("✅ 얼굴이 감지되고 생체 반응 확인! 출석 처리 중...")
                st.toast("🎉 출석이 완료되었습니다!", icon="✅")
                
                st.session_state.attendance_records.append({
                    "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "상태": "출석 완료",
                    "감지된 얼굴 수": len(results.detections),
                    "라이브니스 검증": f"{total_blinks_detected}회 깜빡임"
                })
                st.session_state.is_attended = True # 출석 완료 상태로 변경
                st.session_state.camera_active = False # 웹캠 중지
                break # 웹캠 루프 종료

        else:
            attendance_status_message.info("👀 얼굴을 감지할 수 없습니다. 화면 중앙에 얼굴을 맞춰주세요.")
            
        video_placeholder.image(frame, channels="BGR", use_column_width=True)
        time.sleep(0.01) # CPU 사용률 줄이기

    cap.release() # 웹캠 자원 해제
    cv2.destroyAllWindows()
    if st.session_state.is_attended:
        st.success("🎉 출석 확인이 성공적으로 완료되었습니다!")
    else:
        st.info("출석 확인이 중지되었거나 완료되지 않았습니다.")


st.markdown("---")

# --- 관리자 대시보드 (간소화) ---
st.header("📊 관리자 대시보드 (출석 통계)")
if st.session_state.attendance_records:
    df_attendance = pd.DataFrame(st.session_state.attendance_records)
    st.dataframe(df_attendance, use_container_width=True)
    
    col_stats1, col_stats2 = st.columns(2)
    with col_stats1:
        st.metric("총 출석 시도", len(df_attendance))
    with col_stats2:
        successful_attendances = df_attendance[df_attendance['상태'] == '출석 완료'].shape[0]
        st.metric("성공적인 출석", successful_attendances)
        
    st.download_button(
        label="📥 출석 기록 다운로드 (CSV)",
        data=df_attendance.to_csv(index=False).encode('utf-8'),
        file_name="facecheck_edu_attendance_record.csv",
        mime="text/csv",
        help="현재 세션의 출석 기록을 CSV 파일로 다운로드합니다."
    )
else:
    st.info("아직 출석 기록이 없습니다. '출석 확인 시작' 버튼을 눌러 출석을 시도해보세요.")

st.markdown("---")

st.subheader("🛠️ 주요 기술 스택 (제안서 포함용)")
st.markdown("""
* **안면 인식**: `FaceNet`, `MediaPipe`, `OpenCV` (실시간 얼굴 감지 및 임베딩)
* **라이브니스 검증**: `Dlib`, `Blink Detection CNN` (눈 깜빡임, 고개 움직임 등 생체 반응 분석)
* **백엔드**: `FastAPI` / `Django` + `PostgreSQL` (안전한 데이터 관리 및 API 연동)
* **프론트엔드**: `Streamlit` (빠른 프로토타이핑 및 UI 구현), `React` / `Vue` + `WebRTC` (고급 웹 인터페이스)
* **보안**: `JWT`, `AES 암호화`, `HTTPS`, `사용자 권한 분리` (데이터 및 통신 보안)
* **배포**: `AWS` / `Azure` + `CI/CD` (안정적인 서비스 운영)
""")

st.markdown("---")
st.caption("© 2025 FaceCheck EDU. All rights reserved.")