from langchain.embeddings import HuggingFaceInstructEmbeddings
from pinecone import Pinecone
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI

GoogleAPIKey = st.secrets["GOOGLE_API_KEY"]

llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=GoogleAPIKey, temperature=0.1)

pineconeAPIKey = st.secrets["PINECONE_API_KEY"]

pc = Pinecone(api_key=pineconeAPIKey)

indexName = "riccardo"
index = pc.Index(indexName)

instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")

def Reply(question):
    e = instructor_embeddings.embed_query(question)

    data = index.query(
    vector = e,
    top_k = 3,
    include_values = True
    )

    matches = data['matches']  # Get all matches
    text_parts = []
    # Extract IDs from the first 3 matches
    for match in matches[:3]:
        extracted_id = match['id']
        try:
            fetch = index.fetch([extracted_id])  # Handle potential missing key
            if fetch:
                text_part = fetch['vectors'][extracted_id]['metadata']['text']
                text_parts.append(text_part)
                # print(text_part)  # Print the extracted text part
        except KeyError:
            print(f"ID '{extracted_id}' not found in the index.")


    prompt_template = """

    Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    **Context:**

    {context_part}

    **Question:**

    {question}

    """.format(context_part=text_parts, question=question)

    try:
        # print(prompt_template)
        response = llm.invoke(prompt_template)

        return response
        
    except Exception as e:
        print(f"An error occurred: {e}")


