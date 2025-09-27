from typing import Any, Optional
import litellm
import asyncio
import os

class LitellmModel:
    """
    LiteLLM Model integration for the citizen service chatbot.
    This provides integration with multiple LLM providers via LiteLLM.
    """
    
    def __init__(self, model: str, api_key: str):
        self.model_name = model
        self.api_key = api_key
        
        # Set the API key in environment for LiteLLM
        if "gemini" in model.lower():
            os.environ["GEMINI_API_KEY"] = api_key
        elif "groq" in model.lower():
            os.environ["GROQ_API_KEY"] = api_key
        elif "openai" in model.lower():
            os.environ["OPENAI_API_KEY"] = api_key
    
    async def generate_response(self, query: str, instructions: str = None) -> str:
        """
        Generate a response using LiteLLM with the configured model.
        """
        try:
            # Prepare the messages
            messages = []
            
            if instructions:
                messages.append({
                    "role": "system",
                    "content": instructions
                })
            
            messages.append({
                "role": "user",
                "content": query
            })
            
            # Use LiteLLM for generation
            response = await litellm.acompletion(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"LiteLLM error: {str(e)}"
