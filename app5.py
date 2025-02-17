import streamlit as st
import pandas as pd

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
    st.title("아파트 분양가 예측 AI (Demo) - No OpenAI")

    # 사용자 입력 UI
    region = st.selectbox("지역 선택", ["강남구", "송파구", "부산 해운대구", "대구 수성구"])
    area = st.number_input("면적 (㎡)", value=84, step=1)
    floor = st.number_input("해당 층 수", value=10, step=1)
    built_year = st.number_input("건축 연도", value=2020, step=1)

    st.write("※ 아래 정보는 샘플이며, 실제 모델링 시 추가 변수(학군, 역세권 지수 등)가 필요할 수 있습니다.")

    if st.button("분양가 예측하기"):
        predicted_price = predict_price(region, area, floor, built_year)

        st.subheader("예측 분양가 결과")
        st.write(f"해당 아파트의 예상 분양가는 평당 **{predicted_price}만원** 정도로 추정됩니다.")

if __name__ == "__main__":
    main()