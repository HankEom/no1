import streamlit as st
import pandas as pd
import numpy as np

# ------ UI 스타일 적용 ------
st.set_page_config(
    page_title="정유 공정 AI 분석 Agent",
    page_icon="🔍",
    layout="wide"
)

# ------ 헤더 ------
st.markdown(
    """
    <h1 style='text-align: center; color: #003366;'>🚀 정유 공정 AI 분석 Agent</h1>
    <h5 style='text-align: center; color: #555;'>정유 제품 생산량, 장비 고장 예측, 가격 변동을 AI로 분석하세요.</h5>
    """,
    unsafe_allow_html=True
)
st.divider()

# ------ 데이터 예제 ------
production_data = pd.DataFrame({'month': [1, 2, 3, 4, 5], 'production': [100000, 105000, 110000, 115000, 120000]})
failure_data = pd.DataFrame({'sensor1': [0.7, 0.8, 0.9], 'sensor2': [0.6, 0.9, 0.8], 'temperature': [60, 65, 70], 'failure': [0, 1, 1]})
price_data = pd.DataFrame({'price': [70, 72, 74, 76, 78]})

# ------ 분석 함수 (더미 데이터 기반) ------
def predict_production():
    next_month = production_data['month'].max() + 1
    next_production = int(production_data['production'].mean() * 1.02)  # 단순 평균 + 2%
    return next_month, next_production

def predict_failure():
    failure_risk = np.random.choice(["낮음", "보통", "높음"], p=[0.5, 0.3, 0.2])
    return failure_risk

def predict_price():
    future_price = round(np.mean(price_data['price']) * 1.05, 2)  # 평균 가격 + 5%
    return future_price

# ------ 선택 옵션 ------
st.markdown("<h4 style='color: #003366;'>📊 원하는 분석을 선택하세요:</h4>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📈 정유 제품 생산량 예측"):
        month, production = predict_production()
        st.success(f"📢 다음 달 예상 생산량: **{production:,} 배럴**")

with col2:
    if st.button("정유 공정 장비 고장 예측"):
        risk = predict_failure()
        st.warning(f"🔍 장비 고장 위험도: **{risk}**")

with col3:
    if st.button("💰 정유 제품 가격 예측"):
        price = predict_price()
        st.info(f"💵 향후 3개월 예상 유가: **${price} per barrel**")

# ------ 결과 요약 섹션 ------
st.divider()
st.markdown("<h4 style='color: #003366;'>📌 분석 결과 요약</h4>", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### 📈 생산량 예측")
    st.markdown(f"**🛢️ 예상 생산량:** {predict_production()[1]:,} 배럴")
    
with col_b:
    st.markdown("### ⚙️ 장비 고장 예측")
    st.markdown(f"**🚨 고장 위험도:** {predict_failure()}")

with col_c:
    st.markdown("### 💰 가격 예측")
    st.markdown(f"**📊 예상 유가:** ${predict_price()} per barrel")

st.divider()

# ------ 마무리 문구 ------
st.markdown(
    "<h5 style='text-align: center; color: #555;'>📊 AI 분석 결과를 바탕으로 더욱 스마트한 결정을 내리세요!</h5>",
    unsafe_allow_html=True
)
