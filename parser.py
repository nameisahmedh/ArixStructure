import pdfplumber
import fitz  # PyMuPDF
import io
from PIL import Image
import os
import re
import docx
from pptx import Presentation
from bs4 import BeautifulSoup
import csv

# Create a directory to store extracted images
if not os.path.exists("temp_images"):
    os.makedirs("temp_images")

def clean_text(text):
    """Cleans up extracted text."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_document(file_bytes, filename):
    """
    Main router function that parses a file from bytes and extracts content 
    based on its extension with enhanced data structuring capabilities.
    """
    extension = os.path.splitext(filename)[1].lower()
    
    if extension == '.pdf':
        return _parse_pdf(file_bytes)
    elif extension == '.docx':
        return _parse_docx(file_bytes)
    elif extension == '.pptx':
        return _parse_pptx(file_bytes)
    elif extension == '.txt':
        return _parse_txt(file_bytes)
    elif extension in ['.html', '.htm']:
        return _parse_html(file_bytes)
    elif extension == '.csv':
        return _parse_csv(file_bytes)
    else:
        print(f"Unsupported file type: {extension}")
        return {
            "full_text": f"Error: Unsupported file type '{extension}'. Please upload a supported file format.",
            "tables": [],
            "image_files": [],
            "metadata": {"error": f"Unsupported format: {extension}"}
        }

def _parse_pdf(file_bytes):
    """Enhanced PDF parser with better data structuring."""
    all_text = ""
    all_tables = []
    image_files = []
    metadata = {"pages": 0, "extraction_method": "pdfplumber + fitz"}
    
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            metadata["pages"] = len(pdf.pages)
            print(f"Parsing {len(pdf.pages)} pages...")
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    all_text += f"--- PAGE {i+1} ---\n"
                    all_text += clean_text(page_text)
                    all_text += f"\n--- END PAGE {i+1} ---\n\n"
                
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        clean_table = []
                        for row in table:
                            clean_row = [str(cell).strip() if cell is not None else "" for cell in row]
                            clean_table.append(clean_row)
                        all_tables.append(clean_table)

    except Exception as e:
        print(f"Error with pdfplumber: {e}")
        metadata["extraction_error"] = str(e)

    # Extract images with PyMuPDF
    image_filenames = set()
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page_index in range(len(doc)):
                image_list = doc.get_page_images(page_index)
                for img_index, img in enumerate(image_list):
                    try:
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        image_filename = f"temp_images/img_p{page_index+1}_{img_index}.{image_ext}"
                        with Image.open(io.BytesIO(image_bytes)) as pil_img:
                            pil_img.save(image_filename)
                        image_filenames.add(image_filename)
                    except Exception as e:
                        print(f"Error extracting image: {e}")
    except Exception as e:
        print(f"Error with image extraction: {e}")

    image_files = sorted(list(image_filenames))
    
    return {
        "full_text": all_text,
        "tables": all_tables,
        "image_files": image_files,
        "metadata": metadata
    }

def _parse_docx(file_bytes):
    """Enhanced DOCX parser with table detection and structuring."""
    all_text = ""
    all_tables = []
    metadata = {"extraction_method": "python-docx", "tables_found": 0}
    
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        
        # Extract real tables first
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)
            
            if table_data:
                all_tables.append(table_data)
        
        # Extract text and detect CSV-like structures
        current_csv_table = []
        for para in doc.paragraphs:
            text = para.text.strip()
            all_text += text + "\n"

            if not text:
                continue
            
            # Detect structured data patterns
            if _is_structured_data(text):
                delimiter = ',' if ',' in text else '\t'
                try:
                    f = io.StringIO(text)
                    reader = csv.reader(f, delimiter=delimiter)
                    for row in reader:
                        cleaned_row = [cell.strip() for cell in row if cell.strip()]
                        if len(cleaned_row) > 1:
                            current_csv_table.append(cleaned_row)
                except:
                    pass
            else:
                if current_csv_table:
                    all_tables.append(current_csv_table)
                    current_csv_table = []
        
        # Add final table if exists
        if current_csv_table:
            all_tables.append(current_csv_table)
        
        metadata["tables_found"] = len(all_tables)
            
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        metadata["extraction_error"] = str(e)
    
    return {
        "full_text": clean_text(all_text),
        "tables": all_tables,
        "image_files": [],
        "metadata": metadata
    }

def _parse_pptx(file_bytes):
    """Enhanced PPTX parser with slide structure preservation."""
    all_text = ""
    all_tables = []
    metadata = {"extraction_method": "python-pptx", "slides": 0}
    
    try:
        prs = Presentation(io.BytesIO(file_bytes))
        metadata["slides"] = len(prs.slides)
        
        for slide_idx, slide in enumerate(prs.slides):
            slide_text = f"--- SLIDE {slide_idx + 1} ---\n"
            
            for shape in slide.shapes:
                if hasattr(shape, "text_frame") and shape.text_frame:
                    slide_text += shape.text + "\n"
                
                if hasattr(shape, "table") and shape.table:
                    table_data = []
                    for row in shape.table.rows:
                        row_data = [cell.text.strip() for cell in row.cells]
                        table_data.append(row_data)
                    
                    if table_data:
                        all_tables.append(table_data)
            
            slide_text += f"--- END SLIDE {slide_idx + 1} ---\n\n"
            all_text += slide_text
            
    except Exception as e:
        print(f"Error parsing PPTX: {e}")
        metadata["extraction_error"] = str(e)
    
    return {
        "full_text": clean_text(all_text),
        "tables": all_tables,
        "image_files": [],
        "metadata": metadata
    }

def _parse_txt(file_bytes):
    """Enhanced TXT parser with automatic structure detection."""
    all_text = ""
    all_tables = []
    metadata = {"extraction_method": "text_analysis"}
    
    try:
        all_text = file_bytes.decode('utf-8', errors='ignore')
        
        # Detect structured data in text
        current_table = []
        lines = all_text.splitlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if _is_structured_data(line):
                delimiter = ',' if line.count(',') >= 2 else '\t'
                try:
                    f = io.StringIO(line)
                    reader = csv.reader(f, delimiter=delimiter)
                    for row in reader:
                        cleaned_row = [cell.strip() for cell in row if cell.strip()]
                        if len(cleaned_row) > 1:
                            current_table.append(cleaned_row)
                except:
                    pass
            else:
                if current_table:
                    all_tables.append(current_table)
                    current_table = []
        
        # Add final table
        if current_table:
            all_tables.append(current_table)
        
        metadata["tables_detected"] = len(all_tables)

    except Exception as e:
        print(f"Error parsing TXT: {e}")
        metadata["extraction_error"] = str(e)
    
    return {
        "full_text": all_text,
        "tables": all_tables,
        "image_files": [],
        "metadata": metadata
    }

def _parse_html(file_bytes):
    """Enhanced HTML parser with better table extraction."""
    all_text = ""
    all_tables = []
    metadata = {"extraction_method": "beautifulsoup"}
    
    try:
        soup = BeautifulSoup(file_bytes, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text
        all_text = soup.get_text(separator='\n', strip=True)
        
        # Extract tables with structure preservation
        for table in soup.find_all('table'):
            table_data = []
            
            # Extract all rows
            for row in table.find_all('tr'):
                row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                if row_data:
                    table_data.append(row_data)
            
            if table_data:
                all_tables.append(table_data)
        
        metadata["tables_found"] = len(all_tables)
            
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        metadata["extraction_error"] = str(e)
    
    return {
        "full_text": clean_text(all_text),
        "tables": all_tables,
        "image_files": [],
        "metadata": metadata
    }

def _parse_csv(file_bytes):
    """Parse CSV files with automatic delimiter detection."""
    all_text = ""
    all_tables = []
    metadata = {"extraction_method": "csv_parser"}
    
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                text_content = file_bytes.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            text_content = file_bytes.decode('utf-8', errors='ignore')
        
        all_text = text_content
        
        # Detect delimiter
        sample = text_content[:1024]
        delimiter = ','
        if sample.count('\t') > sample.count(','):
            delimiter = '\t'
        elif sample.count(';') > sample.count(','):
            delimiter = ';'
        
        # Parse CSV
        f = io.StringIO(text_content)
        reader = csv.reader(f, delimiter=delimiter)
        table_data = []
        
        for row in reader:
            if row:  # Skip empty rows
                table_data.append([cell.strip() for cell in row])
        
        if table_data:
            all_tables.append(table_data)
        
        metadata["delimiter_detected"] = delimiter
        metadata["rows_parsed"] = len(table_data)
        
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        metadata["extraction_error"] = str(e)
    
    return {
        "full_text": all_text,
        "tables": all_tables,
        "image_files": [],
        "metadata": metadata
    }

def _is_structured_data(text):
    """Detect if text contains structured data patterns."""
    if not text:
        return False
    
    # Check for common delimiters
    comma_count = text.count(',')
    tab_count = text.count('\t')
    pipe_count = text.count('|')
    semicolon_count = text.count(';')
    
    # Heuristics for structured data
    return (comma_count >= 2 or tab_count >= 2 or 
            pipe_count >= 2 or semicolon_count >= 2)