import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import time

# ---------------------------
# 페이지 기본 설정 (레이아웃, 사이드바 확장 등)
# ---------------------------
st.set_page_config(
    page_title="Five Solutions Demo",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------
# 간단한 CSS 스타일 (배경, 글꼴 크기 등 꾸미기)
# ---------------------------
st.markdown("""
    <style>
    /* 전체 바디 배경색 */
    body {
        background-color: #F7F7F7;
    }
    /* 메인 컨테이너 내부 패딩, 배경 */
    .main .block-container {
        background-color: #FFFFFF;
        padding: 2rem 2rem 2rem 2rem;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    }
    /* 사이드바 배경색 */
    .sidebar .sidebar-content {
        background-color: #314e52;
        color: #FFFFFF;
    }
    /* 사이드바 텍스트 */
    .sidebar .sidebar-content .css-1n543e5 {
        color: #FFFFFF;
    }
    /* 기본 글꼴 크기 조금 키우기 */
    body, label, span, h1, h2, h3, h4 {
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# 사이드바 메뉴 구성
# ---------------------------
menu = st.sidebar.radio(
    "솔루션 선택",
    (
        "1) 입찰/사업관리",
        "2) 시장조사/분석",
        "3) 문서/보고서 작성",
        "4) 자료/콘텐츠 제작",
        "5) 업무도구 연계/자동화",
    )
)

# -------------------------------------------------------------------------------------
# (1) 입찰/사업관리 솔루션
# -------------------------------------------------------------------------------------
def show_bid_management():
    st.markdown("## \u2728 입찰/사업관리 솔루션 (더미 버전) \u2728")
    st.write("여기서는 RFP(입찰제안요청서) 업로드, P/Q 업무 분장표, 발주 동향 등을 **간단히** 시연해봅니다.")
    
    # 파일 업로드 (PDF, Word, etc)는 실제 파싱 없이 시연만
    uploaded_file = st.file_uploader("RFP 파일 업로드(PDF/DOCX)", type=["pdf","docx"])
    
    if uploaded_file is not None:
        st.success(f"파일 `{uploaded_file.name}` 업로드 완료!")
        st.info("실제 로직 연결 시, 파싱된 내용으로 자동 요약/검토가 가능합니다.")
    
    st.markdown("---")
    # 더미 테이블 (P/Q 업무 분장표)
    st.subheader("P/Q 업무 분장표 (예시)")
    dummy_data = {
        "구분": ["기술 제안서", "가격 제안서", "계약 조건 검토"],
        "담당자": ["김영희", "홍길동", "이철수"],
        "마감일": ["2025-03-10", "2025-03-12", "2025-03-15"],
        "상태": ["진행중", "대기", "검토중"]
    }
    df_dummy = pd.DataFrame(dummy_data)
    st.table(df_dummy)
    
    # 국가별 발주동향 (더미)
    st.markdown("---")
    st.subheader("국가별 발주동향 (더미)")
    country = st.selectbox("국가 선택", ["사우디", "인도네시아", "베트남", "기타"])
    st.write(f"**{country}** 발주 동향:")
    st.write("- 대규모 인프라 투자 계획 발표 (더미 데이터)\n- 입찰 시기: 하반기 예정\n- 유관 기관 파트너십 확보 필요")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.success("위 내용은 데모용 더미 데이터입니다. 실제 로직/데이터 연동으로 확장하세요.")

# -------------------------------------------------------------------------------------
# (2) 시장조사/분석 솔루션
# -------------------------------------------------------------------------------------
def show_market_analysis():
    st.markdown("## \u2728 시장조사/분석 솔루션 (더미 버전) \u2728")
    st.write("국가별 지표, 리스크 분석, 건설시장 전망, SWOT 등을 **간단한 차트**로 시연합니다.")
    
    # 간단 더미 차트
    st.markdown("### 예시: 국가별 GDP 추이")
    countries = ["베트남", "인도네시아", "사우디", "브라질"]
    selected_cty = st.selectbox("국가 선택", countries)
    
    # 더미 데이터프레임
    df_gdp = pd.DataFrame({
        "year": [2019, 2020, 2021, 2022, 2023],
        "gdp": [300, 320, 310, 350, 370]
    })
    fig = px.line(df_gdp, x="year", y="gdp", title=f"{selected_cty} GDP 추이 (더미)")
    st.plotly_chart(fig)
    
    st.markdown("### 간단 SWOT 분석 (더미)")
    st.info(f"{selected_cty}에 대한 간단 SWOT 분석 예시를 보여줍니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Strength**: 풍부한 노동력, 성장 가능성\n**Weakness**: 인프라 부족, 규제 미비")
    with col2:
        st.write("**Opportunity**: 해외 투자 유치 증가\n**Threat**: 정치적 불안, 무역 분쟁")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.success("이 역시 Demo용 더미 데이터입니다. 실제 스크래핑/DB 연동 등으로 확장 가능.")

# -------------------------------------------------------------------------------------
# (3) 문서/보고서 작성 솔루션
# -------------------------------------------------------------------------------------
def show_doc_reporting():
    st.markdown("## \u2728 문서/보고서 작성 솔루션 (더미 버전) \u2728")
    st.write("회의록, 보고서 작성 등을 시연. 실제론 NLP나 데이터 연동을 붙여 자동화할 수 있습니다.")
    
    st.markdown("### 회의록 작성 데모 (더미)")
    transcript_text = st.text_area("회의 전사 내용 입력", height=100)
    
    if st.button("회의록(더미) 생성"):
        if transcript_text.strip() == "":
            st.error("회의 내용이 입력되지 않았습니다. 다시 시도하세요.")
        else:
            # 간단한 더미 회의록
            minutes = f"""
[가상의 회의록 초안]
- 회의 개요: 2025-02-14, 해외 프로젝트 논의
- 참석자: 김영희, 홍길동 등
- 주요 내용:
  {transcript_text[:50]}...
- 결정 사항: P/Q 분장, 일정 재확인
- 후속 조치: 시장조사팀 협의, 차주 보고서 제출
"""
            st.success("회의록 초안을 생성했습니다. (더미)")
            st.text(minutes)
            
            st.download_button(
                label="회의록 TXT 다운로드",
                data=minutes.encode('utf-8'),
                file_name="meeting_minutes.txt",
                mime="text/plain"
            )

# -------------------------------------------------------------------------------------
# (4) 자료/콘텐츠 제작 솔루션
# -------------------------------------------------------------------------------------
def show_content_creation():
    st.markdown("## \u2728 자료/콘텐츠 제작 솔루션 (더미 버전) \u2728")
    st.write("PPT 자료, 표/그래프, 슬라이드 구성 등. 여긴 **OpenAI API 없이** 간단한 샘플 UI를 보여줍니다.")
    
    st.markdown("### 발표자료 텍스트 입력")
    content_text = st.text_area("발표자료에 들어갈 내용", height=100)
    
    if st.button("슬라이드(더미) 만들기"):
        if content_text.strip() == "":
            st.warning("내용을 먼저 입력하세요.")
        else:
            st.success("슬라이드 초안을 텍스트로 생성했습니다. (더미)")
            slide_output = f"""
[슬라이드 1]
- 제목: 프로젝트 개요
- 내용: {content_text[:30]}...

[슬라이드 2]
- 시장 분석
- 주요 그래프/표 삽입 (가정)

[슬라이드 3]
- 결론 & 향후 일정
"""
            st.code(slide_output, language="markdown")
            
            # PDF or PPT 다운로드 (여기서는 더미)
            st.download_button(
                label="PPT 파일 (더미) 다운로드",
                data=slide_output.encode('utf-8'),
                file_name="slides_dummy.ppt",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

# -------------------------------------------------------------------------------------
# (5) 업무도구 연계/자동화 솔루션
# -------------------------------------------------------------------------------------
def show_tool_integration():
    st.markdown("## \u2728 업무도구 연계/자동화 솔루션 (더미 버전) \u2728")
    st.write("이메일 작성, 문서 포맷 변환(PDF/Word), 언어 변환 등 **OpenAI 없이** 더미로 구성된 예시입니다.")
    
    # 이메일 작성 더미
    st.subheader("이메일 작성 (더미)")
    recipient = st.text_input("수신자 이메일", value="test@example.com")
    subject = st.text_input("제목", value="해외 발주 보고서 공유드립니다.")
    body = st.text_area("본문 내용", height=100, value="안녕하세요.\n아래와 같이 해외 발주 정보를 공유드립니다...\n감사합니다.")
    
    if st.button("이메일 생성/미리보기"):
        st.success("이메일 미리보기 (더미)")
        st.write(f"**수신:** {recipient}")
        st.write(f"**제목:** {subject}")
        st.text(body)
    
    st.markdown("---")
    # 문서 포맷 변환 (더미)
    st.subheader("문서 포맷 변환 (더미)")
    convert_file = st.file_uploader("문서 업로드 (예: .docx)", type=["docx","pdf","pptx","txt"])
    if convert_file is not None:
        st.info(f"파일 {convert_file.name} 업로드됨. 실제 변환 로직은 구현 필요.")
        if st.button("포맷 변환(더미)"):
            with st.spinner("변환중..."):
                time.sleep(2)
            st.success("문서 변환 완료(가정). PDF 파일(더미) 다운로드가 가능합니다.")
            dummy_pdf = b"PDF binary data (dummy)"
            st.download_button(
                label="PDF 다운로드",
                data=dummy_pdf,
                file_name="converted_dummy.pdf",
                mime="application/pdf"
            )
    
    st.markdown("---")
    # 간단 번역 (더미)
    st.subheader("언어 변환 (더미)")
    text_for_translation = st.text_input("번역할 문장 입력")
    lang_choice = st.selectbox("번역 언어 선택", ["영어", "한국어", "일본어"])
    if st.button("번역(더미)"):
        st.success(f"'{text_for_translation}' → '{lang_choice}' (더미 결과)")
        st.write(f"번역된 문장(예시): [ {text_for_translation[::-1]} ]")  # 글자 뒤집기 등 임의로 처리

# -------------------------------------------------------------------------------------
# Main 실행 로직: 사이드바 메뉴에 따라 함수 호출
# -------------------------------------------------------------------------------------
if menu == "1) 입찰/사업관리":
    show_bid_management()
elif menu == "2) 시장조사/분석":
    show_market_analysis()
elif menu == "3) 문서/보고서 작성":
    show_doc_reporting()
elif menu == "4) 자료/콘텐츠 제작":
    show_content_creation()
elif menu == "5) 업무도구 연계/자동화":
    show_tool_integration()
