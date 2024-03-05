import streamlit as st
from apps.langchain_helper import Reply
import pandas as pd


def app():

    reviewCSV_file_path = "review.csv"
    reviewdf = pd.read_csv(reviewCSV_file_path)

    st.title("Riccardo Q&A")
    phoneNumber = st.text_input("Phone Number: ")
    question = st.text_input("Question: ")



    if question:
        # chain = get_qa_chain()
        response = Reply(question)

        st.header("Answer")
        st.text_area("Edit Response", response, height=100)
                
        new_row = {"prompt": f"{question}", "response": response}

        # Append the new row to the DataFrame using loc
        reviewdf.loc[len(reviewdf)] = new_row

        # Write the DataFrame back to the CSV file
        reviewdf.to_csv(reviewCSV_file_path, index=False)  # Overwrite the existing file

