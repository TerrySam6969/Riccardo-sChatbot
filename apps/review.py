import pandas as pd
import streamlit as st
from langchain.embeddings import HuggingFaceInstructEmbeddings
from pinecone import Pinecone


pineconeAPIKey = st.secrets["PINECONE_API_KEY"]
reviewCSV_file_path = "review.csv"

def app():
    try:
        # Attempt to read the CSV file
        reviewdf = pd.read_csv(reviewCSV_file_path)
        reviewdf["Mark for Deletion"] = [False] * len(reviewdf)
    except:
        st.error("Review Area is empty")

    with st.container():
        edited_df = st.data_editor(
            reviewdf,
            column_config={
                "Mark for Deletion": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select rows to remove",
                    default=False,
                ),
                "ID": "ID",
                "response": "Response",
                "prompt": "Prompt",
            },
            disabled=["ID"],
            hide_index=True,
        )


    # Save filtered DataFrame to a CSV file
    if st.button("Save Edited Data"):
        edited_df.to_csv(reviewCSV_file_path, index=False)  # Save to a new file


    if st.button("Delete", type="primary"):

        # Filter the DataFrame based on marked rows for deletion
        filtered_df = reviewdf[~edited_df["Mark for Deletion"]]
        filtered_df.to_csv(reviewCSV_file_path, index=False)  # Save to a new file

        # Delete rows from the original DataFrame
        reviewdf = reviewdf[~edited_df["Mark for Deletion"]]
        
    # if st.button("Add to database", type="primary"):




