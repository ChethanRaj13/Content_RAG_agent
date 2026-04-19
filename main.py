from langchain_core.documents import Document
import mysql.connector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

def build_text(row):
    return f"""
    Topic: {row['topic']}
    Hook: {row['hook_line']}
    Format: {row['format']}
    Tone: {row['tone']}
    Emotion: {row['emotion_intensity']}
    Purpose: {row['purpose']}
    Content: {row['clean_text']}
    """

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="linkedin_posts_db"
)

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM posts")
rows = cursor.fetchall()

documents = []

for row in rows:
    doc = Document(
        page_content=build_text(row),
        metadata={
            "id": row["id"],
            "topic": row["topic"],
            "tone": row["tone"],
            "format": row["format"],
            "engagement": row["perceived_engagement"]
        }
    )
    documents.append(doc)

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)

vectorstore.persist()

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5
    }
)


llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.7
)


prompt = ChatPromptTemplate.from_template("""
You are a viral content generator.

Study the examples below:

{context}

Now create a high-performing post for:
{question}

Follow similar patterns but do NOT copy.
""")

def format_docs(docs):
    return "\n\n---\n\n".join([doc.page_content for doc in docs])

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
)

response = rag_chain.invoke("Write a LinkedIn post about how i created a viral post using AI agent that i have built.")

print(response.content)