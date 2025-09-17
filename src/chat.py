from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from .embedding import emb_text
from .vector_db_connect import VectorDBConnection, VectorSearch

from config.vectordb_cfg import VectorDBConfig, VectorSearchConfig
from config.model_cfg import EmbeddingConfig, LLMConfig

def chat_with_milvus(question: str, 
                     api_key: str, 
                     chat_history: list = [],
                     cluster_endpoint: str = "http://localhost:19530",
                     token: str = "") -> str:
    # Initialize Milvus connection using the URI from environment variables
    milvus_conn = VectorDBConnection(uri=cluster_endpoint, token=token)
    milvus_client = milvus_conn.get_client()

    vectordb_cfg = VectorDBConfig(embedding_dim=EmbeddingConfig.embedding_dim)
    vector_search_cfg = VectorSearchConfig(limit=3)
    
    # Initialize Vector Search
    collection_name = vectordb_cfg.collection_name
    vector_search = VectorSearch(milvus_client, collection_name)
    
    # Embed the question
    question_vector = emb_text(question, api_key)
    
    # Search in Milvus
    search_results = vector_search.search(query_vector=question_vector, 
                                          limit=vector_search_cfg.limit,
                                          search_params=vector_search_cfg.search_params,
                                          output_fields=vector_search_cfg.output_fields)
    
    print(f"Search results: {search_results}, type: {type(search_results)}")

    retrieved_lines_with_distances = [(res["entity"]["text"], res["distance"]) for res in search_results[0]]

    history_str = None
    if chat_history:
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
    
    # Prepare context from search results
    context = "\n".join([f"{line_with_distance[0]}" for line_with_distance in retrieved_lines_with_distances])
    
    # Initialize Google Generative AI model
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    llm = ChatGoogleGenerativeAI(model=LLMConfig.model_name, 
                                 temperature=LLMConfig.temperature, 
                                 api_key=api_key,
                                 max_retries=2)
    sys_msg = "You are a helpful assistant that helps people find information about Scientific socialism in Marxism and Leninism."

    # Create prompt with context
    prompt = "Chat history:\n{history}\n\nContext:\n{context}\n\nQuestion: {question}\n\nNOTE:\n- If the context is not sufficient to answer the question, please say 'Câu hỏi này không nằm trong nội dung được cung cấp. Vui lòng hỏi câu hỏi khác.' Else if the input is for conversating purpose, just communicate normally.\n- Provide the answer in Vietnamese language only.\n- Provide the header of the context as proof for your answer'.\n- Answer in a friendly way as if you are a teacher.\n- Don't add tag to your answer.\n- Fix any typo in the context before answering.\n- Answer as a markdown.\n- Use line break if necessary.\n\nSample answer:<answer here>\nTrích dẫn:<header here>"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", sys_msg),
        ("human", prompt)
    ])

    chain = prompt_template | llm
    response = chain.invoke(
        {"history": history_str, "context": context, "question": question}
    )

    response_content = response.content if hasattr(response, 'content') else str(response)
    
    # Get response from LLM
    # response = llm.predict(prompt)

    # response = llm.invoke(messages=[
    #     {"role": "system", "content": sys_msg},
    #     {"role": "human", "content": question}
    # ])
    
    return response_content, context