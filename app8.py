import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="아파트 분양가 예측",
    page_icon="🏠",
    layout="wide"
)

# 간단한 CSS 스타일 (선택사항)
st.markdown("""
<style>
/* 배경색, 폰트 등 간단히 꾸며보기 */
body {
    background-color: #f5f7fa;
}
.main > div {
    background: #ffffff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
.title h1 {
    color: #3B3B98;
    font-weight: 700;
}
label {
    font-weight: 600;
    color: #1e1e1e;
}
</style>
""", unsafe_allow_html=True)

def predict_price(region, area, floor, built_year):
    """
    간단한 더미 로직으로 분양가 추정 (실제 모델 대체)
    - 지역, 면적, 층, 건축연도 등의 파라미터를 받아
      임의 공식으로 평당가격을 계산하는 예시
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
    st.title("아파트 분양가 예측 AI")
    st.write("지정된 지역, 면적, 층수, 건축 연도 정보를 바탕으로 간단하게 **평당 분양가**를 예측합니다.")
    st.write("---")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("📝 입력 값 설정")
        region = st.selectbox("지역 선택", ["강남구", "송파구", "부산 해운대구", "대구 수성구"])
        area = st.number_input("면적 (㎡)", value=84, step=1)
        floor = st.number_input("해당 층 수", value=10, step=1)
        built_year = st.number_input("건축 연도", value=2020, step=1)

        st.caption("※ 실제 모델링 시 추가 변수(학군, 역세권, 주변 시세 등)를 반영하면 더욱 정확해질 수 있습니다.")

        if st.button("분양가 예측하기"):
            predicted_price = predict_price(region, area, floor, built_year)
            st.session_state["predicted_price"] = predicted_price
            st.session_state["region"] = region
            st.session_state["area"] = area
            st.session_state["built_year"] = built_year
        else:
            if "predicted_price" not in st.session_state:
                st.session_state["predicted_price"] = None

    with col2:
        st.subheader("🔍 예측 결과")
        if st.session_state.get("predicted_price") is not None:
            st.success(
                f"해당 아파트의 예상 분양가는 평당 **{st.session_state['predicted_price']}만원** 정도로 추정됩니다."
            )
            # 층수 변동 시 어떻게 달라지는지 그래프로 시각화
            floor_values = list(range(1, 31))  # 1층부터 30층까지 예시
            df = pd.DataFrame({
                "floor": floor_values,
                "predicted_price": [
                    predict_price(
                        st.session_state["region"],
                        st.session_state["area"],
                        f,
                        st.session_state["built_year"]
                    ) for f in floor_values
                ]
            })

            chart = alt.Chart(df).mark_line().encode(
                x=alt.X('floor', title='층수'),
                y=alt.Y('predicted_price', title='예측 평당 가격(만원)')
            ).properties(
                title='층수에 따른 분양가 추정 변동'
            )
            st.altair_chart(chart, use_container_width=True)

        else:
            st.info("왼쪽에서 정보를 입력한 뒤 [분양가 예측하기] 버튼을 눌러주세요.")

    st.write("---")
    st.markdown("""
    **© 2025 부동산 AI Lab**  
    - 본 애플리케이션은 교육 및 데모용으로 제작되었습니다.  
    - 실제 가격과 차이가 있을 수 있으므로, 참고 자료로만 활용하시기 바랍니다.
    """)

if __name__ == "__main__":
    main()