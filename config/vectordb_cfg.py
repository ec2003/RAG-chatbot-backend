class VectorDBConfig():
    def __init__(self, 
                 *,
                 embedding_dim: int,
                 uri: str = 'http://localhost:19530',
                 collection_name: str = 'MLN131',
                 consistency_level: str = 'Strong'
                 ):
        self.embedding_dim = embedding_dim
        self.uri = uri
        self.collection_name = collection_name
        self.consistency_level = consistency_level

class VectorIndexConfig():
    def __init__(self,
                 index_type: str = 'HNSW',
                 params: dict[str, str] = {"M": 8, "efConstruction": 64},
                 metric_type: str = "IP",
                 extra_params: dict = {}):
        self.index_type = index_type,
        self.params = params,
        self.metric_type = metric_type,
        self.extra_params = extra_params

    def get_index_params(self):
        return {
            "index_type": self.index_type,
            "params": self.params,
            "metric_type": self.metric_type,
            "extra_params": self.extra_params
        }
        

class VectorSearchConfig():
    def __init__(self,
                 limit: int = 5,
                 search_params: dict = {"metric_type": "COSINE", "params": {"ef": 64}},
                 output_fields: list[str] = ["text"]):
       self.limit = limit
       self.search_params = search_params
       self.output_fields = output_fields

if __name__ == "__main__":
    # vectordb_cfg = VectorDBConfig(embedding_dim=1024)
    # print(vectordb_cfg.__dict__)
    vector_index_cfg = VectorIndexConfig()
    print(vector_index_cfg.get_index_params())
    # vector_search_cfg = VectorSearchConfig()
    # print(vector_search_cfg.__dict__)