"""
Offline AI alternative when HuggingFace is not available
"""
import re
import os
from datetime import datetime

class OfflineAI:
    """Simple rule-based AI for document analysis"""
    
    def __init__(self):
        self.column_patterns = {
            'sales': ['sales', 'revenue', 'income', 'total_sales', 'amount'],
            'date': ['date', 'time', 'day', 'month', 'year', 'created', 'updated'],
            'region': ['region', 'area', 'location', 'place', 'country', 'state'],
            'product': ['product', 'item', 'goods', 'service', 'name'],
            'category': ['category', 'type', 'class', 'group', 'segment'],
            'profit': ['profit', 'margin', 'earnings', 'net'],
            'cost': ['cost', 'price', 'expense', 'fee'],
            'quantity': ['quantity', 'units', 'amount', 'count', 'number'],
            'customer': ['customer', 'client', 'user', 'buyer'],
            'order': ['order', 'transaction', 'purchase', 'id']
        }
    
    def analyze_text(self, prompt, context):
        """Analyze text and provide intelligent responses"""
        prompt_lower = prompt.lower()
        
        # Question type detection
        if any(word in prompt_lower for word in ['what', 'describe', 'tell me about']):
            return self._handle_what_question(prompt_lower, context)
        elif any(word in prompt_lower for word in ['how many', 'count', 'number']):
            return self._handle_count_question(prompt_lower, context)
        elif any(word in prompt_lower for word in ['summary', 'summarize']):
            return self._handle_summary_question(context)
        elif any(word in prompt_lower for word in ['column', 'field', 'extract']):
            return self._handle_column_question(prompt_lower, context)
        else:
            return self._handle_general_question(prompt_lower, context)
    
    def _handle_what_question(self, prompt, context):
        """Handle 'what' questions"""
        if 'about' in prompt:
            # Extract key topics from context
            topics = self._extract_topics(context)
            if topics:
                return f"This document appears to be about: {', '.join(topics[:3])}. It contains structured data with information on various topics."
            else:
                return f"This document contains: {context[:200]}..."
        elif 'table' in prompt or 'data' in prompt:
            return "The document contains structured data tables that can be analyzed and visualized."
        else:
            return "This document contains structured information that can be explored in the Analytics section."
    
    def _handle_count_question(self, prompt, context):
        """Handle counting questions"""
        return "The document contains structured data. Check the Analytics section for detailed statistics including row counts, column counts, and data summaries."
    
    def _handle_summary_question(self, context):
        """Handle summary requests"""
        sentences = [s.strip() for s in context.split('.') if s.strip()][:3]
        if sentences:
            return f"Summary: {'. '.join(sentences)}."
        else:
            return "This document contains structured data that can be analyzed and visualized."
    
    def _handle_column_question(self, prompt, context):
        """Handle column extraction questions"""
        # Extract keywords from prompt
        words = re.findall(r'\b\w+\b', prompt.lower())
        
        suggestions = []
        for word in words:
            for category, patterns in self.column_patterns.items():
                if word in patterns:
                    suggestions.append(category.title())
        
        if suggestions:
            return f"Based on your query, look for columns related to: {', '.join(set(suggestions))}. Use the column search feature in Analytics."
        else:
            return "To find specific columns, try keywords like 'sales', 'date', 'region', 'product', or use exact column names."
    
    def _handle_general_question(self, prompt, context):
        """Handle general questions"""
        return "I can help analyze your document. Try asking: 'What is this about?', 'Summarize the content', or use the Analytics section to explore data directly."
    
    def _extract_topics(self, context):
        """Extract key topics from context"""
        # Common business/data topics
        topics = []
        topic_keywords = {
            'sales data': ['sales', 'revenue', 'profit'],
            'customer information': ['customer', 'client', 'user'],
            'product data': ['product', 'item', 'goods'],
            'financial data': ['cost', 'price', 'expense', 'profit'],
            'geographic data': ['region', 'location', 'country'],
            'time series data': ['date', 'time', 'month', 'year']
        }
        
        context_lower = context.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in context_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def extract_columns(self, query, available_columns):
        """Extract relevant columns based on query"""
        query_lower = query.lower()
        suggested_cols = []
        
        # Direct matching
        for col in available_columns:
            col_lower = col.lower()
            if query_lower in col_lower or col_lower in query_lower:
                suggested_cols.append(col)
        
        # Semantic matching
        if not suggested_cols:
            query_words = re.findall(r'\b\w+\b', query_lower)
            for word in query_words:
                for category, patterns in self.column_patterns.items():
                    if word in patterns:
                        for col in available_columns:
                            if any(pattern in col.lower() for pattern in patterns):
                                if col not in suggested_cols:
                                    suggested_cols.append(col)
        
        return suggested_cols
    
    def describe_image(self, image_path):
        """Generate basic image description"""
        try:
            from PIL import Image
            
            filename = os.path.basename(image_path)
            
            with Image.open(image_path) as img:
                width, height = img.size
                format_name = img.format or "Unknown"
                
                # Basic description
                if width > height:
                    orientation = "landscape"
                elif height > width:
                    orientation = "portrait"
                else:
                    orientation = "square"
                
                return f"{format_name} image ({width}x{height}, {orientation} orientation) extracted from document"
                
        except Exception:
            return "Image file extracted from document"

# Global instance
offline_ai = OfflineAI()