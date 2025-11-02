from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self):
        load_dotenv()
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        os.environ["GROQ_API_KEY"] = self.groq_api_key
        self.primary_model = "openai/gpt-oss-120b"
        self.fallback_model = "llama-3.1-8b-instant"
        self.current_model = self.primary_model

    def get_llm(self, use_fallback=False):
        """
        Get LLM instance. If use_fallback is True, uses the fallback model.
        """
        try:
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY is not set")
            
            model = self.fallback_model if use_fallback else self.current_model
            print(f"Using Groq model: {model}")
            
            llm = ChatGroq(
                api_key=self.groq_api_key,
                model=model,
                temperature=0.7
            )
            return llm
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {str(e)}")
    
    def should_use_fallback(self, error_message):
        """
        Check if error indicates rate limit, then switch to fallback model.
        """
        error_lower = str(error_message).lower()
        # Check for rate limit errors (429, rate limit, tokens per day)
        if any(keyword in error_lower for keyword in [
            'rate limit', 
            '429', 
            'tokens per day', 
            'tpd',
            'limit reached'
        ]):
            print(f"Rate limit detected. Switching to fallback model: {self.fallback_model}")
            self.current_model = self.fallback_model
            return True
        return False