############################################
# Streamlit Demo App for AI Model Selection
# Author: S-Oil AI Team
# Date: 2025-xx-xx
############################################

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time

# -----------------------------
# 1) CSV 업로드: 파일 업로드 및 데이터 미리보기
# -----------------------------
def upload_data():
    uploaded_file = st.file_uploader("① CSV 파일 업로드", type=['csv', 'txt'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("파일 업로드 완료!")
        st.write("미리보기:")
        st.dataframe(df.head())
        return df
    else:
        return None

# -----------------------------
# 2) 모델 선택에 따른 더미데이터 & 결과 생성 함수
# -----------------------------
def generate_regression_results(df):
    """
    가짜 회귀 결과를 생성하여 보여주는 함수
    """
    st.subheader("회귀 모델")
    
    # 가상의 training 과정 시뮬레이션
    with st.spinner("회귀 모델 학습 중..."):
        time.sleep(1.5)
    
    st.write("**가상 RMSE**:", round(np.random.uniform(10, 30), 2))
    st.write("**가상 MAE**:", round(np.random.uniform(5, 15), 2))
    st.write("**가상 R²**:", round(np.random.uniform(0.5, 0.95), 2))
    
    # 가상의 예측 vs 실제 그래프
    x = np.linspace(0, 50, 50)
    real = x + np.random.normal(0, 5, 50)
    pred = x + np.random.normal(0, 5, 50)
    
    chart_data = pd.DataFrame({
        'Index': x,
        '실제값': real,
        '예측값': pred
    })
    line_chart = alt.Chart(chart_data.melt('Index')).mark_line().encode(
        x='Index',
        y='value',
        color='variable'
    ).properties(
        width=600,
        height=300
    )
    st.altair_chart(line_chart, use_container_width=True)

def generate_classification_results(df):
    """
    가짜 분류 결과를 생성하여 보여주는 함수
    """
    st.subheader("분류 모델")
    with st.spinner("분류 모델 학습 중..."):
        time.sleep(1.5)
    
    st.write("**가상 정확도(Accuracy)**:", round(np.random.uniform(0.7, 0.95), 2))
    st.write("**가상 정밀도(Precision)**:", round(np.random.uniform(0.6, 0.95), 2))
    st.write("**가상 재현율(Recall)**:", round(np.random.uniform(0.6, 0.95), 2))
    
    # 혼동행렬 더미
    conf_mat = np.random.randint(10, 100, size=(2,2))
    st.write("**혼동행렬**:")
    st.table(pd.DataFrame(conf_mat, columns=["Predicted:0", "Predicted:1"], 
                                       index=["Actual:0", "Actual:1"]))

def generate_timeseries_results(df):
    """
    가짜 시계열 결과를 생성하여 보여주는 함수
    """
    st.subheader("시계열 모델")
    with st.spinner("시계열 모델 학습 중..."):
        time.sleep(1.5)
    
    st.write("**가상 MAPE**:", round(np.random.uniform(5, 20), 2), "%")
    st.write("**가상 RMSE**:", round(np.random.uniform(10, 35), 2))
    
    # 실제 vs 예측 시계열 차트
    time_index = pd.date_range("2025-01-01", periods=30, freq='D')
    actual_vals = np.random.randint(100, 200, 30)
    pred_vals = actual_vals + np.random.randint(-20, 20, 30)
    
    ts_df = pd.DataFrame({
        'date': time_index,
        '실제값': actual_vals,
        '예측값': pred_vals
    })
    
    ts_chart = alt.Chart(ts_df.melt('date')).mark_line().encode(
        x='date:T',
        y='value:Q',
        color='variable:N'
    ).properties(
        width=600,
        height=300
    )
    st.altair_chart(ts_chart, use_container_width=True)

def generate_clustering_results(df):
    """
    가짜 군집 결과를 생성하여 보여주는 함수
    """
    st.subheader("군집 모델")
    with st.spinner("군집 모델 학습 중..."):
        time.sleep(1.5)
    
    # 가상의 군집 label
    k = 3
    st.write(f"**가상 군집 수**: {k} (예: K-means)")
    dummy_data = pd.DataFrame({
        'x': np.random.normal(loc=range(k), scale=1.0, size=300),
        'y': np.random.normal(loc=range(k), scale=1.0, size=300)
    })
    dummy_data['cluster'] = np.random.randint(0, k, 300)

    # 군집 시각화 (산점도)
    scatter_chart = alt.Chart(dummy_data).mark_circle(size=60).encode(
        x='x:Q',
        y='y:Q',
        color='cluster:N'
    ).properties(
        width=600,
        height=300
    )
    st.altair_chart(scatter_chart, use_container_width=True)

def generate_deep_learning_results(df):
    """
    가짜 딥러닝 결과를 생성하여 보여주는 함수
    """
    st.subheader("딥러닝 모델")
    with st.spinner("딥러닝 모델 학습 중..."):
        time.sleep(2)  # DL은 오래 걸리는 느낌
    
    st.write("**가상 손실(Loss)**:", round(np.random.uniform(0.05, 0.5), 3))
    st.write("**가상 정확도/MAE/RMSE**:", round(np.random.uniform(0.6, 0.95), 2))
    
    # 에폭별 손실 감소 그래프
    epochs = list(range(1, 11))
    loss_vals = np.linspace(start=np.random.uniform(0.3, 0.8), stop=np.random.uniform(0.05, 0.2), num=10)
    loss_df = pd.DataFrame({'epoch': epochs, 'loss': loss_vals})
    
    loss_chart = alt.Chart(loss_df).mark_line().encode(
        x='epoch',
        y='loss'
    ).properties(
        width=600,
        height=300
    )
    st.altair_chart(loss_chart, use_container_width=True)

# -----------------------------
# 3) GPT로 리포트 요약·코드 수정 (더미 응답)
# -----------------------------
def gpt_summary_section():
    st.subheader("④ S-Oil GPT")

    user_query = st.text_input("GPT에게 물어보세요 (예: 결과를 한 문장으로 요약해줘)", "")
    if st.button("GPT에게 요청"):
        with st.spinner("GPT 요약 요청 중..."):
            time.sleep(1.5)  # 실제 API 대기 시뮬레이션
        # 더미 응답
        gpt_answer = """
        [GPT(가상) 응답] 
        모델 성능은 현재 매우 양호합니다. 
        만약 정확도를 높이고 싶다면, 하이퍼파라미터 튜닝을 통해 오버피팅을 방지하고, 
        데이터 전처리를 더 정교하게 수행할 것을 권장합니다.
        """
        st.success(gpt_answer)

    code_improvement = st.checkbox("코드 개선 아이디어 받기")
    if code_improvement:
        with st.spinner("GPT 코드 개선안 요청 중..."):
            time.sleep(1.5)
        # 더미 코드 수정안
        improved_code = """
        # GPT가 제안한 개선안
        # 1. Dropout 레이어 추가
        # 2. Learning Rate Scheduler 도입
        # 3. EarlyStopping 콜백 적용
        """
        st.info("아래는 GPT가 제안한 코드 수정 아이디어입니다:")
        st.code(improved_code, language='python')

# -----------------------------
# Streamlit Main
# -----------------------------
def main():
    st.title("데모: All-in-One AI Web App")
    st.write("""
    **UI 흐름**:
    1) CSV 업로드 
    2) 모델 선택(회귀·분류·시계열·군집·딥러닝)
    3) 훈련·평가 및 해석(결과 그래프/지표)
    4) GPT로 리포트 요약·코드 수정
    """)

    df = upload_data()
    model_option = st.selectbox("② 원하는 모델을 선택하세요",
                   ["- 선택 없음 -", "회귀(Regression)", "분류(Classification)",
                    "시계열(Time Series)", "군집(Clustering)", "딥러닝(Deep Learning)"])

    # 3) 모델 학습·평가·해석
    if model_option != "- 선택 없음 -":
        st.markdown("---")
        st.subheader("③ 모델 훈련·평가 및 해석")
        if df is not None:
            # 실제로는 df를 모델에 입력해야 하지만, 본 코드는 제안서용이므로 더미함수 호출
            if model_option == "회귀(Regression)":
                generate_regression_results(df)
            elif model_option == "분류(Classification)":
                generate_classification_results(df)
            elif model_option == "시계열(Time Series)":
                generate_timeseries_results(df)
            elif model_option == "군집(Clustering)":
                generate_clustering_results(df)
            elif model_option == "딥러닝(Deep Learning)":
                generate_deep_learning_results(df)
        else:
            st.warning("CSV 파일을 업로드해주세요.")

    # 4) GPT로 리포트 요약·코드 수정
    st.markdown("---")
    gpt_summary_section()

if __name__ == "__main__":
    main()
