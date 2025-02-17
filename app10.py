import streamlit as st
import pandas as pd
import altair as alt
import random

# 1) 페이지 기본 설정 (브라우저 탭 제목, 아이콘, 레이아웃)
st.set_page_config(
    page_title="국내외 건설분야 동향 리서치",
    page_icon="🏗️",
    layout="wide"
)

# 2) 간단한 CSS 스타일 (배경색, 폰트 등) - 필요 시 확장 가능
st.markdown("""
<style>
body {
    background-color: #f9fafc;
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


def get_mock_data(query: str):
    """
    사용자가 입력한 '건설 동향' 관련 검색어(query)에 대응하는
    데이터(기사/리포트 목록, 감성 점수, 트렌드 지표 등)를 반환하는 함수.
    """

    # (예시) 임의의 기사 키워드 / 감성 점수 / 트렌드 수치 생성
    random_keywords = ["스마트시티", "친환경 건설", "해외 수주", "공공사업", "민간투자", "AI 건설자동화"]
    random.shuffle(random_keywords)  # 키워드 순서 임의화

    # 기사 예시 데이터 5건 생성
    data = []
    for i in range(5):
        data.append({
            "제목": f"[{query}] {random_keywords[i]} 관련 동향",
            "키워드": random_keywords[i],
            "기사/리포트 출처": f"신문사{random.randint(1,5)}",
            "감성 점수": round(random.uniform(-1, 1), 2),
            "조회수": random.randint(100, 3000)
        })

    df = pd.DataFrame(data)
    return df

def generate_trend_chart_data():
    """
    월별 기사량 같은 간단한 트렌드 시계열 데이터를 만들어서 시각화에 활용.
    """
    months = ["2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06"]
    trend_counts = [random.randint(50, 200) for _ in months]
    df_trend = pd.DataFrame({"월": months, "기사수": trend_counts})
    return df_trend

def generate_keyword_freq_data(df_articles: pd.DataFrame):
    """
    기사 테이블(키워드 열)을 바탕으로, 각 키워드의 빈도를 집계하는 예시.
    """
    freq_series = df_articles["키워드"].value_counts().reset_index()
    freq_series.columns = ["키워드", "빈도"]
    return freq_series

def main():
    st.title("국내외 건설분야 동향 리서치 AI")
    st.write("""
    본 페이지는 **국내외 건설분야 동향**을 검색/시각화하는 솔루션입니다.
    """)

    st.write("---")
    
    # 검색 기능: 사용자에게 검색 키워드 입력받기
    query = st.text_input("검색어를 입력하세요 (예: 건설, 해외 수주 등)", value="건설")

    # 검색 버튼
    if st.button("동향 검색"):
        # (1) 기사/리포트 더미 데이터 가져오기
        df_articles = get_mock_data(query)

        st.subheader("1. 기사/리포트 목록")
        st.caption("검색 키워드를 기반으로 한 예시 기사 데이터")
        st.dataframe(df_articles, use_container_width=True)

        # (2) 월별 기사 수 트렌드 차트
        st.subheader("2. 월별 기사량 추이")
        st.caption("최근 6개월 간 기사/리포트량을 가정한 시계열 데이터")
        df_trend = generate_trend_chart_data()
        
        line_chart = alt.Chart(df_trend).mark_line(point=True).encode(
            x=alt.X("월", sort=None),
            y="기사수"
        ).properties(
            width=600,
            height=300,
            title="월별 기사수 변화"
        )
        st.altair_chart(line_chart, use_container_width=True)

        # (3) 키워드별 빈도 (막대 그래프)
        st.subheader("3. 키워드별 빈도")
        st.caption("이번 검색 결과에 등장한 주요 키워드 빈도")
        df_freq = generate_keyword_freq_data(df_articles)
        bar_chart = alt.Chart(df_freq).mark_bar().encode(
            x=alt.X("키워드", sort="-y"),
            y="빈도",
            tooltip=["키워드", "빈도"]
        ).properties(
            width=600,
            height=300,
            title="키워드 빈도 분석"
        )
        st.altair_chart(bar_chart, use_container_width=True)

        # (4) 간단한 요약/해석 (더미)
        st.subheader("4. 간단한 동향 요약 (예시)")
        st.write(f"""
        - 검색 키워드: **{query}**  
        - 기사 데이터에서 **{', '.join(df_articles['키워드'].unique())}** 등의 
          키워드가 주로 등장하였습니다.  
        - 전체 감성 점수는 평균 **{round(df_articles['감성 점수'].mean(), 2)}** 정도로, 
          (음수면 부정, 양수면 긍정)  
        - 최근 6개월 기사량은 월 평균 **{int(df_trend['기사수'].mean())}건** 수준이며, 
          전월 대비 소폭 변동이 있는 것으로 보입니다.
        """)
    else:
        st.info("검색어 입력 후 [동향 검색] 버튼을 눌러주세요.")

    st.write("---")
    st.markdown("""
    **© 2025 건설 AI Lab**  
    - 본 애플리케이션은 교육/시연을 위해 제작된 **UI 데모**입니다.  
    - 실제 분석/LLM 활용 등을 추가하면 **동향 리서치 AI**로 확장 가능합니다.
    """)

if __name__ == "__main__":
    main()
