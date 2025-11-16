import streamlit as st
import requests
import os
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceClient:
    def __init__(self):
        self.token = self._get_token()
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        self.base_url = "https://api-inference.huggingface.co/models/"
        
    def _get_token(self):
        """Securely get HF token from secrets or environment"""
        try:
            # Try Streamlit secrets first
            return st.secrets["HF_TOKEN"]
        except (KeyError, AttributeError):
            # Fallback to environment variable
            token = os.getenv("HF_TOKEN")
            if not token:
                logger.warning("HF_TOKEN not found. AI features will be limited.")
            return token
    
    def _query_api(self, model, payload, retries=3):
        """Query HF API with retry logic"""
        if not self.token:
            return None
            
        url = self.base_url + model
        
        for attempt in range(retries):
            try:
                response = requests.post(url, headers=self.headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 503:
                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    return {"error": "Model loading"}
                else:
                    logger.error(f"API error: {response.status_code}")
                    return None
                    
            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")
                if attempt == retries - 1:
                    return None
                time.sleep(1)
        
        return None

# Initialize client
hf_client = HuggingFaceClient()

def get_text_response(prompt, context):
    """Generate AI response using HuggingFace"""
    if not hf_client.token:
        return "AI service not configured. Please add HF_TOKEN to secrets.toml"
    
    # Use text generation model
    payload = {
        "inputs": f"Context: {context[:800]}\n\nQuestion: {prompt}\n\nAnswer:",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    result = hf_client._query_api("microsoft/DialoGPT-medium", payload)
    
    if result:
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "").strip()
        elif "error" in result:
            if result["error"] == "Model loading":
                return "AI model is starting up. Please try again in a moment."
    
    # Fallback to summarization for document questions
    if "what" in prompt.lower() and "about" in prompt.lower():
        payload = {
            "inputs": context[:1000],
            "parameters": {"max_length": 100, "min_length": 20}
        }
        
        result = hf_client._query_api("facebook/bart-large-cnn", payload)
        
        if result and isinstance(result, list) and len(result) > 0:
            summary = result[0].get("summary_text", "")
            if summary:
                return f"This document is about: {summary}"
    
    return "Unable to process your question at the moment. Please try again."

def get_image_descriptions(image_paths):
    """Get image descriptions using HuggingFace"""
    descriptions = []
    
    for img_path in image_paths:
        if not hf_client.token:
            descriptions.append({
                "path": img_path,
                "description": "AI service not configured"
            })
            continue
            
        try:
            # Validate path to prevent traversal
            safe_path = os.path.abspath(img_path)
            temp_dir = os.path.abspath("temp_images")
            if not safe_path.startswith(temp_dir):
                descriptions.append({"path": img_path, "description": "Invalid image path"})
                continue
                
            with open(safe_path, "rb") as f:
                img_data = f.read()
            
            response = requests.post(
                hf_client.base_url + "nlpconnect/vit-gpt2-image-captioning",
                headers=hf_client.headers,
                data=img_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    desc = result[0].get("generated_text", "Visual content")
                else:
                    desc = "Visual content"
            else:
                desc = "Image analysis unavailable"
                
        except (requests.RequestException, IOError, OSError) as e:
            logger.error(f"Image processing error: {e}")
            desc = "Image processing failed"
        
        descriptions.append({"path": img_path, "description": desc})
    
    return descriptions

def get_image_query_response(prompt, image_descriptions):
    """Answer questions about images"""
    if not image_descriptions:
        return "No images found in the document."
    
    context = "\n".join([f"Image {i+1}: {img['description']}" for i, img in enumerate(image_descriptions)])
    return get_text_response(prompt, f"Document images: {context}")

def get_specific_table_indices(prompt, tables_as_text, num_tables):
    """Select table indices based on prompt"""
    import re
    
    prompt_lower = prompt.lower()
    
    if "all" in prompt_lower:
        return "all"
    
    # Extract table numbers
    numbers = re.findall(r'table\s*(\d+)', prompt_lower)
    if not numbers:
        numbers = re.findall(r'\b(\d+)\b', prompt)
    
    if numbers:
        indices = [str(max(0, int(n) - 1)) for n in numbers if 0 < int(n) <= num_tables]
        if indices:
            return ", ".join(indices)
    
    if "first" in prompt_lower:
        return "0"
    elif "last" in prompt_lower:
        return str(num_tables - 1)
    
    return "all"