from langchain_google_genai import ChatGoogleGenerativeAI
from config.model_cfg import LLMConfig

def verify_api_key(api_key: str) -> bool:
    try:
        llm = ChatGoogleGenerativeAI(model=LLMConfig.model_name, temperature=LLMConfig.temperature, api_key=api_key, max_retries=1)
        test_prompt = "Hello, how are you?"
        response = llm.predict(test_prompt)
        return True if response else False
    except Exception as e:
        print(f"API key verification failed: {e}")
        return False