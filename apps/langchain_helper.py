from langchain.embeddings import HuggingFaceInstructEmbeddings
from pinecone import Pinecone

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
import os

load_dotenv()  # take environment variables from .env
GoogleAPIKey = os.environ.get("GOOGLE_API_KEY")

llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=GoogleAPIKey, temperature=0.1)

pc = Pinecone(api_key='847c2b46-aa21-4d21-85de-c659bb6c8810')

indexName = "riccardo"
index = pc.Index(indexName)

instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")


def Reply(question):
    e = instructor_embeddings.embed_query("How do you suggest I put the sample on my resume? put a link to google drive?")

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


