class EmbeddingConfig():
    model_name: str = "AITeamVN/Vietnamese_Embedding"
    embedding_dim: int = 3072
    # max_seq_length: int = 2048

class LLMConfig():
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.2