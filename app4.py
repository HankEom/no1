import streamlit as st
import openai
import pickle
import pandas as pd
import numpy as np

# 벡터 스토어/임베딩 라이브러리 예시
from chromadb.config import Settings
import chromadb

# (예) 사전에 학습된 회귀 모델 로드
with open('trained_model.pkl', 'rb') as f:
    price_model = pickle.load(f)

# 오픈AI API 키 설정 (실사용 시 안전하게 보관!)
openai.api_key = st.secrets["OPENAI_API_KEY"]  # 또는 환경변수

# Chroma DB 예시 설정
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))
collection = chroma_client.get_collection("real_estate_news")

def get_text_context(region_query):
    """
    region_query(예: "서울 강남 개발 정보") 를 기반으로
    벡터 DB에서 관련 텍스트를 검색 → 상위 k개 문서 요약
    """
    # 벡터DB에서 검색
    results = collection.query(query_texts=[region_query], n_results=3)
    docs = results["documents"][0] if results["documents"] else []

    # 여러 문서 합쳐서 GPT 요약 요청
    if docs:
        joined_docs = "\n\n".join(docs)
        prompt = (
            f"다음 텍스트는 {region_query}와 관련된 기사/자료입니다.\n"
            f"이 정보가 해당 지역 아파트 분양가에 어떤 영향을 미칠 가능성이 있는지 요약/분석해줘:\n\n"
            f"{joined_docs}\n\n"
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"system","content":"You are a real estate analyst."},
                      {"role":"user","content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    else:
        return "관련 텍스트 데이터를 찾지 못했습니다."

def predict_price(model, region_code, area, floor, built_year):
    """
    간단한 회귀 모델로 분양가 예측 (예시)
    model: 사전에 학습된 회귀 모델
    region_code, area, floor, built_year 등 숫자/범주형 입력
    """
    input_df = pd.DataFrame([{
        "region_code": region_code,
        "area": area,
        "floor": floor,
        "built_year": built_year
        # 실제로는 추가 변수 필요
    }])
    pred = model.predict(input_df)[0]
    return round(pred, 2)

def main():
    st.title("아파트 분양가 예측 AI (Demo)")

    # 사용자 입력 UI
    region = st.selectbox("지역 선택", ["강남구", "송파구", "부산 해운대구", "대구 수성구"])
    area = st.number_input("면적 (㎡)", value=84, step=1)
    floor = st.number_input("해당 층 수", value=10, step=1)
    built_year = st.number_input("건축 연도", value=2020, step=1)

    st.write("※실제 모델링 시 추가 변수(학군, 역세권 지수 등)가 필요할 수 있습니다.")

    if st.button("분양가 예측하기"):
        # (A) 구조화 모델 예측
        # region_code는 임시로 가정
        region_code_map = {"강남구": 1101, "송파구": 1102, "부산 해운대구": 2601, "대구 수성구": 2701}
        region_code = region_code_map[region]

        predicted_price = predict_price(price_model, region_code, area, floor, built_year)

        st.subheader("예측 분양가 결과")
        st.write(f"해당 아파트의 예상 분양가는 평당 **{predicted_price}만원** 정도로 추정됩니다.")

        # (B) 텍스트 RAG + GPT 요약
        st.subheader("개발/이슈 정보 분석")
        context_summary = get_text_context(region + " 개발 호재")
        st.write(context_summary)

        st.info("※ 위 분석은 예시 GPT 응답이며, 실제 정책/개발 정보와 다를 수 있습니다.")

if __name__ == "__main__":
    main()
