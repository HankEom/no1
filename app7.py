import streamlit as st
import pandas as pd

# 페이지 설정 (브라우저 탭 제목, 아이콘, 레이아웃 등)
st.set_page_config(
    page_title="아파트 분양가 예측",
    page_icon="🏠",
    layout="wide"  # "centered" | "wide"
)

# 간단한 스타일 설정 (배경색, 글씨체 등)
# 필요 시 CSS를 확장해 더 꾸밀 수 있음
st.markdown("""
    <style>
    /* 페이지 전체 배경색 */
    body {
        background-color: #f5f7fa;
    }
    /* 메인 컨테이너 배경, 테두리, 패딩 등 */
    .main > div {
        background: #ffffff;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    /* 헤더 타이틀 커스텀 */
    .title h1 {
        color: #3B3B98;
        font-weight: 700;
    }
    /* Streamlit 기본 위젯 레이블 스타일 */
    label {
        font-weight: 600;
        color: #1e1e1e;
    }
    </style>
""", unsafe_allow_html=True)


def predict_price(region, area, floor, built_year):
    """
    AI로 분양가 추정
    - 지역, 면적, 층, 건축연도 등의 파라미터를 받아
      임의 공식으로 평당가격을 계산
    """
    base_price = 1000  # 기준 가격(만원)
    
    # 지역별 가중치(예시)
    region_factor = {
        "강남구": 3.0,
        "송파구": 2.8,
        "부산 해운대구": 2.2,
        "대구 수성구": 1.8
    }
    
    # 간단한 가중치 계산 예시
    # (면적이 넓을수록, 층수가 높을수록, 건축연도가 최근일수록 가격이 오르는 가정)
    price = (base_price 
             * region_factor[region] 
             * (area / 84) 
             * (1 + (floor - 10) * 0.01) 
             * (1 + (built_year - 2020) * 0.01))
    
    return round(price, 2)


def main():
    # 페이지 상단에 타이틀/설명
    st.title("아파트 분양가 예측 AI")
    st.write("지정된 지역, 면적, 층수, 건축 연도 정보를 바탕으로 간단하게 **평당 분양가**를 예측합니다.")
    st.write("---")

    # 사이드바 or 메인 영역에 입력 옵션을 둘 수 있습니다.
    # 여기서는 메인 영역에 2개 컬럼을 만들어서 왼쪽은 입력, 오른쪽은 결과를 표시해봅니다.
    col1, col2 = st.columns([1, 1.5])  # 비율 조정 가능

    with col1:
        st.subheader("📝 입력 값 설정")
        region = st.selectbox("지역 선택", ["강남구", "송파구", "부산 해운대구", "대구 수성구"])
        area = st.number_input("면적 (㎡)", value=84, step=1)
        floor = st.number_input("해당 층 수", value=10, step=1)
        built_year = st.number_input("건축 연도", value=2020, step=1)

        st.caption("※ 실제 모델링 시 추가 변수(학군, 역세권, 주변 시세 등)를 반영하면 더욱 정확해집니다.")

        if st.button("분양가 예측하기"):
            predicted_price = predict_price(region, area, floor, built_year)
            st.session_state["predicted_price"] = predicted_price
        else:
            # 버튼을 누르기 전에는 예측 결과가 없도록 세션 변수 초기화
            if "predicted_price" not in st.session_state:
                st.session_state["predicted_price"] = None

    with col2:
        st.subheader("🔍 예측 결과")
        if st.session_state.get("predicted_price") is not None:
            st.success(
                f"해당 아파트의 예상 분양가는 평당 **{st.session_state['predicted_price']}만원** 정도로 추정됩니다."
            )
        else:
            st.info("왼쪽에서 정보를 입력한 뒤 [분양가 예측하기] 버튼을 눌러주세요.")

    # 하단 추가 정보/참고 안내
    st.write("---")
    st.markdown("""
    **© 2025 부동산 AI Lab**  
    - 본 애플리케이션은 교육 및 데모용으로 제작되었습니다.  
    - 실제 가격과 차이가 있을 수 있으므로, 참고 자료로만 활용하시기 바랍니다.
    """)
    

if __name__ == "__main__":
    main()