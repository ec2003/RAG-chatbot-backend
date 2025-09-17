from pymilvus import MilvusClient

class VectorDBConnection():
    """
    A class to manage connection to the Milvus vector database.
    """
    def __init__(self, 
                 uri: str = "http://localhost:19530",
                 token: str = None):
        self.client = self.connect_to_milvus(uri, token)
        pass


    @staticmethod
    def connect_to_milvus(uri: str = "http://localhost:19530", token: str = None) -> MilvusClient:
        """
        Connect to the Milvus vector database.

        Args:
            uri (str): The URI of the Milvus server.

        Returns:
            MilvusClient: An instance of the Milvus client.
        """
        client = MilvusClient(uri=uri, token=token)
        return client
    
    def get_client(self) -> MilvusClient:
        """
        Get the Milvus client instance.

        Returns:
            MilvusClient: The Milvus client instance.
        """
        return self.client
    
class VectorSearch():
    """
    A class to perform vector search operations in the Milvus database.
    """
    def __init__(self, milvus_client: MilvusClient, collection_name: str):
        self.milvus_client = milvus_client
        self.collection_name = collection_name

    def search(self, query_vector: list, limit: int = 3, search_params: dict = None, output_fields: list = None):
        """
        Perform a vector search in the specified collection.

        Args:
            query_vector (list): The query vector for the search.
            limit (int): The maximum number of results to return.
            search_params (dict): Additional search parameters.
            output_fields (list): Fields to return in the search results.

        Returns:
            list: A list of search results.
        """
        if search_params is None:
            search_params = {"metric_type": "COSINE", "params": {"ef": 64}}
        if output_fields is None:
            output_fields = ["text"]

        search_results = self.milvus_client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=limit,
            search_params=search_params,
            output_fields=output_fields,
        )
        return search_results