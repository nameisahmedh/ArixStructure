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
                        time.sleep(2 ** attempt)
                        continue
                    return {"error": "Model loading"}
                elif response.status_code == 410:
                    logger.warning(f"Model {model} is deprecated, trying alternative")
                    return {"error": "Model deprecated"}
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
    """Generate AI response using HuggingFace with latest models"""
    if not hf_client.token:
        return "AI service not configured. Please add HF_TOKEN to secrets.toml"
    
    model = "google/flan-t5-large"
    
    # Simple prompt for better results
    simple_prompt = f"Context: {context[:400]}\n\nQuestion: {prompt}\nAnswer:"
    
    try:
        payload = {
            "inputs": simple_prompt,
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.3,
                "do_sample": False,
                "return_full_text": False
            }
        }

        result = hf_client._query_api(model, payload)

        if result and "error" not in result and isinstance(result, list):
            if len(result) > 0 and "generated_text" in result[0]:
                response = result[0]["generated_text"].strip()
                if response and len(response) > 5:
                    return response
    except Exception as e:
        logger.warning(f"Model {model} failed: {e}")
    
    return _get_smart_response(prompt, context)

def _get_smart_response(prompt, context):
    """Smart rule-based responses when AI is unavailable"""
    prompt_lower = prompt.lower()
    
    # Extract column names for column-related queries
    if any(word in prompt_lower for word in ['column', 'field', 'extract']):
        # Simple column extraction logic
        words = prompt_lower.split()
        potential_columns = []
        
        # Look for common column indicators
        column_keywords = ['sales', 'revenue', 'profit', 'date', 'time', 'region', 'category', 'product', 'name', 'id', 'amount', 'price', 'cost']
        
        for word in words:
            if word in column_keywords:
                potential_columns.append(word.title())
        
        if potential_columns:
            return f"Found potential columns: {', '.join(potential_columns)}. Check the available columns in the data preview."
    
    # Context-aware responses
    if "what" in prompt_lower:
        if "about" in prompt_lower:
            return f"This document appears to contain: {context[:150]}..."
        elif "column" in prompt_lower:
            return "This document contains structured data with multiple columns. Check the Analytics section to see all available columns."
    elif "how many" in prompt_lower:
        return "The document contains structured data. Visit the Analytics section to see row and column counts."
    elif "summary" in prompt_lower or "summarize" in prompt_lower:
        sentences = context.split('.')[:3]
        return f"Summary: {'. '.join(sentences)}..."
    elif "table" in prompt_lower:
        return "This document contains data tables. Use the Analytics page to explore and visualize the data."
    elif "extract" in prompt_lower and "column" in prompt_lower:
        return "To extract columns, describe what type of data you're looking for (e.g., 'sales data', 'date columns', 'financial information')."
    
    return "AI service temporarily unavailable. Try: 'What is this about?', 'Summarize the content', or use the Analytics section to explore data directly."

def get_image_descriptions(image_paths):
    """Get image descriptions using HuggingFace with latest models"""
    descriptions = []
    model = "Salesforce/blip-image-captioning-large"
    
    for img_path in image_paths:
        if not hf_client.token:
            descriptions.append({
                "path": img_path,
                "description": "AI image analysis not configured"
            })
            continue
            
        desc = _get_basic_image_description(img_path)
        try:
            # Validate path
            safe_path = os.path.abspath(img_path)
            temp_dir = os.path.abspath("temp_images")
            if not safe_path.startswith(temp_dir):
                descriptions.append({"path": img_path, "description": "Invalid image path"})
                continue
                
            with open(safe_path, "rb") as f:
                img_data = f.read()
            
            response = requests.post(
                hf_client.base_url + model,
                headers=hf_client.headers,
                data=img_data,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_desc = result[0].get("generated_text", "")
                    if generated_desc and len(generated_desc) > 5:
                        desc = generated_desc
            elif response.status_code != 410:  # Not deprecated
                logger.warning(f"Image model {model} returned {response.status_code}")
                
        except (requests.RequestException, IOError, OSError) as e:
            logger.error(f"Image processing error: {e}")
            desc = "Image processing failed"
        
        descriptions.append({"path": img_path, "description": desc})
    
    return descriptions

def _get_basic_image_description(img_path):
    """Generate basic image description from filename and properties"""
    try:
        from PIL import Image
        
        filename = os.path.basename(img_path)
        
        with Image.open(img_path) as img:
            width, height = img.size
            format_name = img.format or "Unknown"
            
            # Basic description based on properties
            if width > height:
                orientation = "landscape"
            elif height > width:
                orientation = "portrait"
            else:
                orientation = "square"
            
            return f"{format_name} image ({width}x{height}, {orientation} orientation)"
            
    except Exception:
        return "Image file extracted from document"

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