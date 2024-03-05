from langchain_google_genai import GoogleGenerativeAI

api_key = 'AIzaSyBuRJ9yWwRjFqC4GDHPg4OsTMEgxOVavcg' # get this free api key from https://makersuite.google.com/
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.1)

# llm = GooglePalm(google_api_key=api_key, temperature=0.1)

from pinecone import Pinecone

pc = Pinecone(api_key='847c2b46-aa21-4d21-85de-c659bb6c8810')

indexName = "riccardo"
index = pc.Index(indexName)


from langchain.embeddings import HuggingFaceInstructEmbeddings

instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")

e = instructor_embeddings.embed_query("How do you suggest I put the sample on my resume? put a link to google drive?")

data = index.query(
  vector= e,
  top_k=3,
  include_values=True
)

matches = data['matches']  # Get all matches

# Extract IDs from the first 3 matches
for match in matches[:3]:
    extracted_id = match['id']
    print(f"Extracted ID: {extracted_id}")

    fetch = index.fetch(["0c75b6a3-2632-4d57-9764-3f44dbb11e2c"])

text_part = fetch['vectors']['0c75b6a3-2632-4d57-9764-3f44dbb11e2c']['metadata']['text']
print(text_part)


question = "How do you suggest I put the sample on my resume? put a link to google drive?"
prompt_template = """

Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

**Context:**

{context_part}

**Question:**

{question}

""".format(context_part=text_part, question=question)

try:
    response = llm.invoke(prompt_template)
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")