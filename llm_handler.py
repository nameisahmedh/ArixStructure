import streamlit as st
import os
import logging
import google.generativeai as genai
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = self._get_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.vision_model = genai.GenerativeModel('gemini-pro-vision')

    def _get_api_key(self):
        """Securely get Gemini API key from secrets or environment"""
        try:
            return st.secrets["GEMINI_API_KEY"]
        except (KeyError, AttributeError):
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.warning("GEMINI_API_KEY not found. AI features will be limited.")
            return api_key

    def generate_text(self, prompt):
        """Generate text using the Gemini Pro model"""
        if not self.api_key:
            return None
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini text generation failed: {e}")
            return None

    def describe_image(self, image_path, prompt):
        """Generate a description for an image using Gemini Pro Vision"""
        if not self.api_key:
            return None
        try:
            img = Image.open(image_path)
            response = self.vision_model.generate_content([prompt, img])
            return response.text
        except Exception as e:
            logger.error(f"Gemini image description failed: {e}")
            return None

gemini_client = GeminiClient()

def get_text_response(prompt, context):
    """Generate AI response using Google Gemini"""
    if not gemini_client.api_key:
        return "AI service not configured. Please add GEMINI_API_KEY to secrets.toml"
    
    full_prompt = f"Context: {context[:4000]}\n\nQuestion: {prompt}\nAnswer:"
    response = gemini_client.generate_text(full_prompt)
    
    if response:
        return response
    
    return _get_smart_response(prompt, context)

def _get_smart_response(prompt, context):
    """Smart rule-based responses when AI is unavailable"""
    prompt_lower = prompt.lower()
    
    if "what" in prompt_lower:
        if "about" in prompt_lower:
            return f"This document appears to contain: {context[:150]}..."
    elif "summary" in prompt_lower or "summarize" in prompt_lower:
        sentences = context.split('.')[:3]
        return f"Summary: {'. '.join(sentences)}..."
    
    return "AI service temporarily unavailable. Try asking a different question."

def get_image_descriptions(image_paths):
    """Get image descriptions using Google Gemini"""
    descriptions = []
    
    for img_path in image_paths:
        if not gemini_client.api_key:
            descriptions.append({
                "path": img_path,
                "description": "AI image analysis not configured"
            })
            continue

        prompt = "Describe this image in detail."
        description = gemini_client.describe_image(img_path, prompt)
        
        if not description:
            description = _get_basic_image_description(img_path)

        descriptions.append({"path": img_path, "description": description})
    
    return descriptions

def _get_basic_image_description(img_path):
    """Generate basic image description from filename and properties"""
    try:
        filename = os.path.basename(img_path)
        return f"Image file: {filename}"
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
