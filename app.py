import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

st.set_page_config(layout="wide")
st.title("👩‍💼 퇴사 가능성 예측 대시보드")

# 1. 데이터 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 데이터 미리보기")
    st.dataframe(df.head())

    # 2. EDA: 시각화
    st.subheader("📈 주요 특성 시각화")
    col1, col2 = st.columns(2)
    with col1:
        if 'JobRole' in df.columns:
            st.write("직무별 이직 여부")
            fig, ax = plt.subplots()
            sns.countplot(data=df, x='JobRole', hue='Attrition', ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    with col2:
        if 'Age' in df.columns:
            st.write("나이별 퇴사자 분포")
            fig, ax = plt.subplots()
            sns.histplot(data=df, x='Age', hue='Attrition', multiple='stack', bins=20, ax=ax)
            st.pyplot(fig)

    # 3. 모델 학습
    st.subheader("🧠 퇴사 예측 모델 실행")

    if 'Attrition' in df.columns:
        df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})

        # 간단한 전처리
        df_clean = pd.get_dummies(df.dropna(), drop_first=True)
        target = 'Attrition'
        X = df_clean.drop(target, axis=1)
        y = df_clean[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        st.text("모델 성능 요약:")
        st.text(classification_report(y_test, y_pred))

        # 4. 전체 데이터에 대한 예측
        df['PredictedAttrition'] = model.predict(df_clean.drop('Attrition', axis=1))

        st.subheader("📋 퇴사 가능성 예측 결과")
        st.dataframe(df[['EmployeeNumber', 'JobRole', 'Age', 'Attrition', 'PredictedAttrition']])

        # 5. 필터링 기능
        st.subheader("🔍 퇴사 가능성이 높은 직원 필터")
        threshold = st.slider("퇴사 예측 기준값 (0=낮음, 1=높음)", 0.0, 1.0, 0.5, 0.05)

        proba = model.predict_proba(df_clean.drop('Attrition', axis=1))[:, 1]
        df['AttritionProbability'] = proba

        filtered = df[df['AttritionProbability'] >= threshold]
        st.dataframe(filtered.sort_values("AttritionProbability", ascending=False))

else:
    st.info("👆 퇴사 데이터가 포함된 CSV 파일을 업로드해주세요.")
