# from sentence_transformers import SentenceTransformer
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# from config.model_cfg import EmbeddingConfig

# embedding_model = SentenceTransformer(f"{EmbeddingConfig.model_name}")
# embedding_model.max_seq_length = EmbeddingConfig.max_seq_length

def emb_text(text, api_key):
    embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", google_api_key=api_key)
    return embedding_model.embed_query(text)