import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("construction_schedule_data.csv")  # 건설 일정 데이터
    return df

df = load_data()

# 제목
st.title("📊 건설 프로젝트 일정 지연 예측 대시보드")

# 데이터 미리보기
st.subheader("📌 데이터 미리보기")
st.write(df.head())

# 지연 요인 분석
st.subheader("📌 일정 지연 주요 요인 분석")

# 상관관계 분석 시각화 (Seaborn 대신 Matplotlib 사용)
st.write("📌 **상관관계 분석 (Correlation Matrix)**")

fig, ax = plt.subplots(figsize=(8, 6))
corr_matrix = df.corr()
cax = ax.matshow(corr_matrix, cmap="coolwarm")
fig.colorbar(cax)

ax.set_xticks(range(len(corr_matrix.columns)))
ax.set_yticks(range(len(corr_matrix.columns)))
ax.set_xticklabels(corr_matrix.columns, rotation=90)
ax.set_yticklabels(corr_matrix.columns)

st.pyplot(fig)

# 지연 일수 분포 시각화
fig = px.histogram(df, x="actual_duration", nbins=30, title="실제 소요 기간 분포")
st.plotly_chart(fig)

# 예측 모델 학습
st.subheader("📌 일정 지연 예측 모델")

# 모델 학습
X = df[['planned_duration', 'weather_delay', 'worker_availability', 'equipment_availability']]
y = df['actual_duration']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 예측 및 평가
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 모델 평가 결과 표시
st.write(f"📌 **평균 절대 오차 (MAE):** {mae:.2f}일")
st.write(f"📌 **R² Score:** {r2:.2f}")

# 중요 변수 시각화 (Seaborn 대신 Plotly 활용)
feature_importance = pd.DataFrame({"Feature": X.columns, "Importance": model.feature_importances_})
fig = px.bar(feature_importance, x="Importance", y="Feature", orientation="h", title="📌 변수 중요도")
st.plotly_chart(fig)
