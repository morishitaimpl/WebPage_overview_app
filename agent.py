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