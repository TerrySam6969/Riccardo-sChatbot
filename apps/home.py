import streamlit as st
from apps.langchain_helper import Reply


def app():
    st.title("Riccardo Q&A")
    phoneNumber = st.text_input("Phone Number: ")
    question = st.text_input("Question: ")



    if question:
        # chain = get_qa_chain()
        response = Reply(question)

        st.header("Answer")
        st.text_area("Edit Response", response, height=100)
