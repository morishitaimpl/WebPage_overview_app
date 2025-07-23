import tiktoken, traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
# from langchain_community.document_loaders import YoutubeLoder
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import config as cf
# import os
# print(os.getenv("ANTHROPIC_API_KEY"))

AI_prompt = """
以下は、あるWebページの本文内容です。
この内容をもとに、各セクションごとに重要なポイントを簡潔に整理し、要点を箇条書きでまとめてください。
ただし、Webページの構成や論調に応じて、単なる箇条書きだけでなく、必要に応じてセクション単位でのまとまりを意識した形式で要約してください。
{content}
日本語で書いてね！
"""

def init_page():
    st.set_page_config(
        page_title = "Website Summarizer"
    )
    st.header("Website Summarizer")
    st.sidebar.title("Options")

def select_model():
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)

    models = ("Claude 3.5 Sonnet", "Claude 3.7 Sonnet", "Claude Sonnet 4", "Claude Opus 4")
    model = st.sidebar.radio("モデルを選択してください:", models)
    
    if model == "Claude 3.5 Sonnet":
        st.session_state.model_name = "claude-3-5-sonnet-20240620"
        return ChatAnthropic(
            temperature=temperature,
            # top_p = top_p,
            # top_k = top_k,
            model_name=st.session_state.model_name,
            max_tokens = 8192
        )
    elif model == "Claude 3.7 Sonnet":
        st.session_state.model_name = "claude-3-7-sonnet-20250219"
        return ChatAnthropic(
            temperature=temperature, 
            # top_p = top_p,
            # top_k = top_k,
            model_name=st.session_state.model_name,
            max_tokens = 32000
        )
    elif model == "Claude Sonnet 4":
        st.session_state.model_name = "claude-sonnet-4-20250514"
        return ChatAnthropic(
            temperature=temperature,
            # top_p = top_p,
            # top_k = top_k,
            model_name=st.session_state.model_name,
            max_tokens = 64000
        )
    elif model == "Claude Opus 4":
        st.session_state.model_name = "claude-opus-4-20250514"
        return ChatAnthropic(
            temperature=temperature,
            # top_p = top_p,
            # top_k = top_k,
            model_name=st.session_state.model_name,
            max_tokens = 64000
        )

def init_chain():
    llm = select_model()
    st.session_state.llm = llm
    prompt = ChatPromptTemplate.from_messages([
        ("user", AI_prompt),
    ])
    output_parser = StrOutputParser()
    return prompt | st.session_state.llm | output_parser

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_content(url):
    try:
        with st.spinner("Fetching Website..."):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            if soup.main:
                return soup.main.get_text()
            elif soup.article:
                return soup.article.get_text()
            else:
                return soup.body.get_text()
    except:
        st.write(traceback.format_exc())
        return None

def main():
    cf.init_page()
    chain = cf.init_chain()

    if url := st.text_input("URL: ", key = "input"):
        is_valid_url = cf.validate_url(url)
        if not is_valid_url:
            st.write("Please input valid url")
        else:
            if content := cf.get_content(url):
                st.markdown("## Summary")
                st.write_stream(chain.stream({"content": content}))
                st.markdown("---")
                st.markdown("### Original Text")
                st.write(content)

if __name__ == "__main__":
    main()