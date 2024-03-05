import pandas as pd
import streamlit as st
from langchain.embeddings import HuggingFaceInstructEmbeddings
from pinecone import Pinecone

pineconeAPIKey = st.secrets["PINECONE_API_KEY"]

def app():
    pc = Pinecone(api_key=pineconeAPIKey)

    instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
    indexName = "riccardo"
    df = pd.read_csv("CombinedQnA12.csv")
    df["Mark for Deletion"] = [False] * len(df)
    with st.container():
        edited_df = st.data_editor(
            df,
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
        changed_rows = edited_df[
        ((edited_df["prompt"] != df["prompt"]) | (edited_df["response"] != df["response"]))
        ]
        changed_ids = changed_rows["ID"].to_list()
        st.write("Changed rows: ", changed_ids)
        if changed_ids:
            st.write(f"IDs of rows with changes in prompt or response: {changed_ids}")

            # Prepare data for upserting
            data_for_upsert = []
            index = pc.Index(indexName)  # Access the Pinecone index

            for row_id in changed_ids:
                changed_row = edited_df[edited_df["ID"] == row_id]
                prompt = changed_row["prompt"].values[0]
                response = changed_row["response"].values[0]

                # Vectorize prompt and response using your defined function
                vec = instructor_embeddings.embed_query(prompt)  # Replace with your vectorization code
                textMeta = f"prompt: {prompt}\nresponse: {response}"

                # Create a dictionary with the ID, embedding, and metadata
                vector_data = {
                    "id": row_id,
                    "values": vec,
                    "metadata": {
                        "text": textMeta
                    }
                }

                data_for_upsert.append(vector_data)
            
            index.upsert(
                vectors=data_for_upsert
            )


        edited_df.to_csv("CombinedQnA12.csv", index=False)  # Save to a new file


    if st.button("Delete", type="primary"):
        # Get IDs of rows marked for deletion
        marked_rows = edited_df[edited_df["Mark for Deletion"]]
        deleted_ids = marked_rows["ID"].to_list()  # Extract a list of IDs

        # Filter the DataFrame based on marked rows for deletion
        filtered_df = df[~edited_df["Mark for Deletion"]]
        filtered_df.to_csv("CombinedQnA12.csv", index=False)  # Save to a new file

        # Delete rows from the original DataFrame
        df = df[~edited_df["Mark for Deletion"]]

        # Use the extracted IDs for any further actions
        if deleted_ids:
            index.delete(ids=deleted_ids)
            st.write(f"Deleted row IDs: {deleted_ids}")
            # You can perform additional actions with these IDs, such as sending them to a database or logging them.

