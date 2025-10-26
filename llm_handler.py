# import streamlit as st
# from huggingface_hub import InferenceClient
# import os
# import time
# import re

# # --- Initialize the Hugging Face Client ---
# try:
#     client = InferenceClient(token=st.secrets["HF_TOKEN"])
# except Exception as e:
#     st.error(f"Failed to initialize Hugging Face client: {e}")

# # --- Define the models we'll use (free tier) ---
# TEXT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
# VISION_MODEL = "Salesforce/blip-image-captioning-large"


# def get_text_response(prompt, context):
#     """
#     Sends a text prompt and context to Mistral-7B.
#     Asks for a plain text response.
#     """
#     try:
#         full_prompt = f"""
#         [INST] You are an expert AI assistant. You will be given the full text of a document
#         and a user's question. Your job is to answer the user's question based
#         ONLY on the document's text.

#         - **Provide a detailed, structured answer.**
#         - **Do NOT use Markdown (like **bold** or ## headers).**
#         - **Use clear, plain text, with newlines for formatting.**
#         - If the answer requires bullet points, use simple dashes (-).
        
#         --- DOCUMENT CONTEXT ---
#         {context}
#         --- END OF CONTEXT ---
        
#         Here is the user's question:
#         Question: {prompt} [/INST]
#         """
        
#         response = client.chat_completion(
#             messages=[{"role": "user", "content": full_prompt}],
#             model=TEXT_MODEL,
#             max_tokens=1024,
#             temperature=0.1
#         )
#         return response.choices[0].message.content
        
#     except Exception as e:
#         if "is currently loading" in str(e):
#             st.warning("The free model is loading. Please wait 10-20 seconds and ask again.")
#             return "The AI model is warming up. Please try your request again in a moment."
#         print(f"Error analyzing text with Hugging Face: {e}")
#         return f"Error analyzing text: {e}"

# def get_image_descriptions(image_paths):
#     """
#     Sends images to the vision model and gets descriptions.
#     """
#     descriptions = []
#     for i, img_path in enumerate(image_paths):
#         try:
#             response = client.image_to_text(image=img_path, model=VISION_MODEL)
            
#             if response and isinstance(response, list) and "generated_text" in response[0]:
import streamlit as st
from huggingface_hub import InferenceClient
import os
import time
import re

# --- Initialize the Hugging Face Client ---
try:
    client = InferenceClient(token=st.secrets["HF_TOKEN"])
except Exception as e:
    st.error(f"Failed to initialize Hugging Face client: {e}")

# --- Define the models we'll use (free tier) ---
TEXT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
VISION_MODEL = "Salesforce/blip-image-captioning-large"


def get_text_response(prompt, context):
    """
    Sends a text prompt and context to Mistral-7B.
    Asks for a plain text response.
    """
    try:
        full_prompt = f"""
        [INST] You are an expert AI assistant. You will be given the full text of a document
        and a user's question. Your job is to answer the user's question based
        ONLY on the document's text.

        - **Provide a detailed, structured answer.**
        - **Do NOT use Markdown (like **bold** or ## headers).**
        - **Use clear, plain text, with newlines for formatting.**
        - If the answer requires bullet points, use simple dashes (-).
        
        --- DOCUMENT CONTEXT ---
        {context}
        --- END OF CONTEXT ---
        
        Here is the user's question:
        Question: {prompt} [/INST]
        """
        
        response = client.chat_completion(
            messages=[{"role": "user", "content": full_prompt}],
            model=TEXT_MODEL,
            max_tokens=1024,
            temperature=0.1
        )
        return response.choices[0].message.content
        
    except Exception as e:
        if "is currently loading" in str(e):
            st.warning("The free model is loading. Please wait 10-20 seconds and ask again.")
            return "The AI model is warming up. Please try your request again in a moment."
        print(f"Error analyzing text with Hugging Face: {e}")
        return f"Error analyzing text: {e}"

def get_image_descriptions(image_paths):
    """
    Sends images to the vision model and gets descriptions.
    """
    descriptions = []
    for i, img_path in enumerate(image_paths):
        try:
            response = client.image_to_text(image=img_path, model=VISION_MODEL)
            
            if response and isinstance(response, list) and "generated_text" in response[0]:
                desc = response[0]["generated_text"]
            else:
                desc = "Could not get a description."

            descriptions.append({
                "path": img_path,
                "description": desc
            })
            
        except Exception as e:
            if "is currently loading" in str(e):
                st.warning("The free image model is loading. Please wait a moment...")
                pass
            print(f"Error describing image {img_path}: {e}")
            descriptions.append({
                "path": img_path,
                "description": f"Error analyzing this image."
            })
    return descriptions

def get_image_query_response(prompt, image_descriptions):
    """
    Answers questions *about* the images using their descriptions.
    Asks for a plain text response.
    """
    context = "\n".join([f"Image: {img['path']}, Description: {img['description']}" for img in image_descriptions])
    
    full_prompt = f"""
    [INST] You are an AI assistant. You will be given a list of image descriptions
    from a document and a user's question about those images.
    
    - **Answer the question based ONLY on the descriptions.**
    - **Do NOT use Markdown.** Use plain text.
    
    --- IMAGE CONTEXT ---
    {context}
    --- END OF CONTEXT ---
    
    Question: {prompt} [/INST]
    """
    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": full_prompt}],
            model=TEXT_MODEL,
            max_tokens=512,
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        if "is currently loading" in str(e):
            return "The AI model is warming up. Please try your request again in a moment."
        return f"Error querying images: {e}"

def get_specific_table_indices(prompt, tables_as_text, num_tables):
    """
    Asks the LLM to identify the *indices* of the table(s) the user wants.
    Returns a comma-separated string of 0-based indices, or "all".
    """
    context = ""
    for i, table_text in enumerate(tables_as_text):
        context += f"--- TABLE {i} ---\n{table_text}\n\n"
    
    full_prompt = f"""
    [INST] You are a table-selection AI. You will be given a user's prompt
    and a list of tables (with their 0-based index numbers).
    The total number of tables is {num_tables}.
    
    Your ONLY job is to return a comma-separated list of 0-based index
    numbers for the table(s) that best answer the user's prompt.
    
    - **Handle 1-based requests:** If the user asks for "the 1st table", return "0".
      If the user asks for "1st and 2nd table", return "0, 1".
    - **Handle "last" requests:** If the user asks for "the last table" and
      there are 7 tables (indices 0-6), return "6".
    - **Handle context requests:** If the user asks for "the table with project features",
      look at the table context and return its index (e.g., "3").
    - **Handle "all" requests:** If the user asks for "all tables" or "any tables",
      or if no specific table matches, return the word "all".
    - **Return ONLY the indices or "all".** Do not add any other text.
    
    --- TABLES ---
    {context}
    --- END OF TABLES ---
    
    User Prompt: {prompt}
    [/INST]
    """
    
    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": full_prompt}],
            model=TEXT_MODEL,
            max_tokens=50, # Room for a few numbers
            temperature=0.0
        )
        result = response.choices[0].message.content.strip().lower()
        
        # --- NEW, MORE ROBUST CLEANING LOGIC ---
        
        if "all" in result:
            return "all"
        
        # Remove all characters that are NOT digits or commas
        cleaned_result = re.sub(r'[^\d,]', '', result)

        if cleaned_result:
            # Final check: make sure it's not just empty commas
            indices = [s.strip() for s in cleaned_result.split(',') if s.strip().isdigit()]
            if indices:
                return ", ".join(indices)
            else:
                return "all" # Failed to find valid numbers
        else:
            return "all" # Default to all if confused or empty
        # --- END OF NEW LOGIC ---

    except Exception as e:
        if "is currently loading" in str(e):
            return "loading"
        print(f"Error selecting table: {e}")
        return "all" # Default to all on error

