# rag_backend.py

import psycopg2
from sentence_transformers import SentenceTransformer
import ollama

# Load embedding model
embedding_model = SentenceTransformer("all-mpnet-base-v2")

# DB connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Prompt
def build_prompt(context, question):
    return f"""
Use only the context below.

Context:
{context}

Question:
{question}

Answer in short and mention source.
"""

# LLM (Llama)
def generate_answer(prompt):
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# RAG pipeline
def rag_pipeline(question):
    try:
        # Step 1: Query embedding
        query_embedding = embedding_model.encode(question)

        # Step 2: Convert to pgvector format (IMPORTANT)
        query_vector = "[" + ",".join(map(str, query_embedding.tolist())) + "]"

        # Step 3: Retrieve from PostgreSQL
        cursor.execute(
        """
        SELECT chunk_text, source
        FROM rag_chunks
        ORDER BY embedding <-> %s::vector
        LIMIT 3
        """,
        (query_vector,)
        )

        results = cursor.fetchall()

    except Exception as e:
        conn.rollback()   # Reset DB state
        print("Error:", e)
        return "Error occurred", []

    # Step 4: Build context
    context = ""
    sources = set()

    for row in results:
        context += f"[Source: {row[1]}]\n{row[0]}\n\n"
        sources.add(row[1])

    # Step 5: Prompt
    prompt = build_prompt(context, question)

    # Step 6: Generate answer
    answer = generate_answer(prompt)

    return answer,sources