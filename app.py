import streamlit as st
import openai
import smtplib
from email.mime.text import MIMEText

# openai.api_key = "YOUR_API_KEY"

def generate_email_content(summary_text, language="ko"):
    prompt = f"""
    아래 요약 내용을 바탕으로, {language}로 된 이메일 초안을 작성해줘.
    형식:
    - 인사말
    - 본문
    - 결론(요청사항, 감사인사)
    
    요약내용:
    {summary_text}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=250
    )
    return response.choices[0].text.strip()

def main():
    st.title("업무도구 연계/자동화 - 이메일 자동작성 & 번역")
    st.write("GPT를 활용해 특정 내용으로 이메일 초안을 자동 생성합니다.")
    
    summary_input = st.text_area("이메일 초안에 반영할 요약/핵심내용 입력")
    language = st.selectbox("언어 선택", ["ko","en","ja","zh"])
    
    if st.button("이메일 작성"):
        with st.spinner("이메일 초안 생성 중..."):
            draft = generate_email_content(summary_input, language)
        st.subheader("생성된 이메일 초안")
        st.write(draft)
        
        # 실제 이메일 전송 로직 (예시)
        # if st.button("이메일 전송"):
        #     sender = "your_email@company.com"
        #     receiver = "receiver@company.com"
        #     msg = MIMEText(draft, _charset="utf-8")
        #     msg["Subject"] = "자동 생성 이메일"
        #     msg["From"] = sender
        #     msg["To"] = receiver
        #     with smtplib.SMTP("smtp.server.com", 587) as server:
        #         server.login("username","password")
        #         server.send_message(msg)
        #     st.success("이메일 전송 완료!")
    
    st.markdown("---")
    st.info("문서 포맷 변환(PDF, Word) 및 다른 업무툴(RPA 등) 연계도 확장 가능.")

if __name__ == "__main__":
    main()