# Viral Content Generator(RAG AI-Agent)

## Purpose

The **Viral Content Generator** project leverages state-of-the-art AI techniques to generate high-performing social media posts based on historical data. By analyzing past LinkedIn posts from a database, the system can generate new viral content tailored to specific topics, tones, formats, and emotional intensities. This project utilizes a combination of embeddings, vector databases, and large language models to create content that resonates with a target audience.

## Main Functionality

1. **Data Extraction**: The project connects to a MySQL database and fetches historical LinkedIn posts stored in a table (`posts`). Each post contains various fields such as `topic`, `hook_line`, `tone`, and `clean_text`.
   
2. **Document Creation**: The posts are then transformed into `Document` objects, which encapsulate the content along with metadata such as the post's topic, tone, and perceived engagement.

3. **Text Embedding and Storage**: The documents are embedded using a pre-trained HuggingFace embedding model (`all-MiniLM-L6-v2`). These embeddings are then stored in a Chroma vector store for efficient similarity search.

4. **Retrieval**: A retrieval mechanism is set up using the Chroma vector store. The system searches for the top 5 most similar documents to a given prompt, enabling the generation of contextually relevant content.

5. **Content Generation**: The system utilizes a pre-trained LLM (`llama3.2:latest`) to generate new posts. The LLM is provided with a prompt that combines the retrieved documents and a user-specified question, guiding it to create a new post in the same style but with original content.

6. **Output**: The system outputs a high-performing LinkedIn post based on the input prompt, emulating the patterns of past successful posts.

## Flow of the Code

1. **Database Connection**: The script connects to a local MySQL database (`localhost:3306`) using credentials provided (e.g., `root` and `password`).
   
2. **Data Fetching**: A SQL query (`SELECT * FROM posts`) retrieves all rows from the `posts` table, which contain LinkedIn post data.

3. **Document Creation**: For each post, the `build_text` function formats the data into a string, which is then wrapped in a `Document` object.

4. **Embeddings and Vector Store**: The documents are passed through a HuggingFace embedding model to generate vector embeddings, which are stored in a Chroma vector store located in the `./chroma_db` directory.

5. **Retrieval and Prompting**: A retriever is set up to pull the top 5 most relevant documents from the Chroma vector store. The retrieved documents are then passed to a `ChatPromptTemplate` to format the data for the language model.

6. **Content Generation**: The language model (`llama3.2:latest`) is invoked to generate a high-performing LinkedIn post based on the provided prompt. The resulting post is printed as the final output.

## Conclusion

This project demonstrates how AI can be used to automate the creation of viral content by learning from past successful posts. By combining the power of vector embeddings, document retrieval, and language models, the system can generate highly engaging posts tailored to specific user needs. It provides a scalable solution for businesses or individuals looking to optimize their social media presence using AI-driven content generation.
