import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 페이지 제목
st.title("📊 건설 프로젝트 일정 지연 예측 대시보드")

# 더미 데이터 생성
np.random.seed(42)
dummy_data = pd.DataFrame({
    "project_id": np.arange(1, 101),
    "planned_duration": np.random.randint(30, 365, 100),
    "actual_duration": np.random.randint(30, 400, 100),
    "weather_delay": np.random.randint(0, 50, 100),
    "worker_availability": np.random.choice([0, 1], 100),
    "equipment_availability": np.random.choice([0, 1], 100),
    "predicted_delay": np.random.randint(0, 50, 100)  # 예측값 더미 데이터
})

# 데이터 미리보기
st.subheader("📌 데이터 미리보기")
st.write(dummy_data.head())

# 📊 프로젝트별 실제 소요 기간 vs 계획된 기간 비교
st.subheader("📌 실제 vs 계획된 공정 기간 비교")
fig1 = px.scatter(dummy_data, x="planned_duration", y="actual_duration", 
                  size="weather_delay", color="worker_availability",
                  title="📌 계획된 기간 vs 실제 소요 기간")
st.plotly_chart(fig1)

# 📅 예측된 일정 지연 분포
st.subheader("📌 예측된 일정 지연 분포")
fig2 = px.histogram(dummy_data, x="predicted_delay", nbins=20, title="📅 예측된 지연 일수 분포")
st.plotly_chart(fig2)

# 🔍 주요 변수 중요도 (랜덤 데이터 활용)
st.subheader("📌 주요 일정 지연 요인 분석")
feature_importance = pd.DataFrame({
    "Feature": ["weather_delay", "worker_availability", "equipment_availability"],
    "Importance": np.random.rand(3) * 100
})
fig3 = px.bar(feature_importance, x="Importance", y="Feature", orientation="h", title="🔍 변수 중요도")
st.plotly_chart(fig3)

st.write("✅ **데이터 분석 대시보드**")
