import os
import fitz  # PyMuPDF
import json
import re
import io
import base64
import time
from PIL import Image

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def get_groq_client():
    if not GROQ_AVAILABLE:
        return None
    api_key = os.environ.get("GROQ_API_KEY")
    return Groq(api_key=api_key) if api_key else None


def get_openrouter_client():
    if not OPENAI_AVAILABLE:
        return None
    api_key = os.environ.get("OPENROUTER_API_KEY")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key) if api_key else None


def is_body_text(text):
    text = text.strip()
    return len(text) > 60 or text.count('\n') >= 2


def get_column_bounds(rect, page_width):
    col_mid = (rect.x0 + rect.x1) / 2
    is_full_width = (0.35 * page_width < col_mid < 0.65 * page_width) or (rect.width > page_width * 0.6)
    
    if is_full_width:
        return 0, page_width
    else:
        if col_mid < page_width / 2:
            return 0, page_width / 2
        else:
            return page_width / 2, page_width


def cols_overlap(x0a, x1a, x0b, x1b):
    return max(0, min(x1a, x1b) - max(x0a, x0b)) > 0


def rect_area(r):
    if r.is_empty: return 0
    return max(0, r.x1 - r.x0) * max(0, r.y1 - r.y0)


def identify_architecture_figures_groq(client, captions):
    if not captions:
        return []
    prompt = """Given the following list of figure captions from an academic paper, identify which figures represent the overall method architecture, pipeline, system overview, or framework. 
Return a JSON object with a single key "architecture_figures" containing a list of figure IDs (strings). Do not include any other text.
Example: {"architecture_figures": ["Figure 1", "Figure 3"]}

Captions:
"""
    for cap in captions:
        prompt += f"[{cap['id']}]: {cap['text']}\n"
        
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return data.get("architecture_figures", [])
    except Exception as e:
        print(f"  Groq API error: {e}")
        return None


def identify_architecture_figures_heuristic(caption_blocks):
    keywords = ['overview', 'architecture', 'pipeline', 'framework', 'method', 'approach', 'schematic', 'system', 'model']
    arch_figures = []
    for cap in caption_blocks:
        if any(kw in cap['text'].lower() for kw in keywords):
            arch_figures.append(cap['id'])
    return arch_figures


def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def is_architecture_diagram_openrouter(client, image):
    try:
        base64_image = encode_image_to_base64(image)
        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-11b-vision-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Look at this image from a research paper. Is it a neural network architecture diagram, system framework, or pipeline overview? Answer with only 'yes' or 'no'."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            max_tokens=10,
            temperature=0.0
        )
        return 'yes' in response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"  OpenRouter API Error during classification: {e}")
        return True  # Fallback to true if API fails


def extract_architecture_diagrams(papers_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    groq_client = get_groq_client()
    or_client = get_openrouter_client()
    
    print("-" * 50)
    print(f"Starting extraction from {papers_dir}")
    if groq_client:
        print("-> Using Groq (Llama 3 70B) for text-based caption filtering.")
    else:
        print("-> Using keyword heuristics for caption filtering (GROQ_API_KEY not set).")
        
    if or_client:
        print("-> Using OpenRouter (Vision) for final image verification.")
    else:
        print("-> Skipping visual verification (OPENROUTER_API_KEY not set).")
    print("-" * 50)

    for filename in os.listdir(papers_dir):
        if not filename.lower().endswith(".pdf"):
            continue
            
        pdf_path = os.path.join(papers_dir, filename)
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"Failed to open {pdf_path}: {e}")
            continue
        
        paper_name = os.path.splitext(filename)[0]
        print(f"\nProcessing {paper_name}...")
        
        all_captions = []
        caption_blocks = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            try:
                blocks = page.get_text("blocks")
            except Exception:
                continue
            
            for block in blocks:
                if block[6] == 0:  # Text block
                    text = block[4].strip()
                    match = re.match(r'^(?:Figure|Fig\.)\s*(\d+[a-zA-Z]?)', text, re.IGNORECASE)
                    if match:
                        fig_id = f"Figure {match.group(1)}"
                        all_captions.append({"id": fig_id, "text": text.replace('\n', ' ')})
                        caption_blocks.append({
                            "id": fig_id,
                            "text": text.replace('\n', ' '),
                            "page_num": page_num,
                            "rect": fitz.Rect(block[:4]),
                            "block_tuple": block
                        })
        
        if not caption_blocks:
            continue
            
        arch_fig_ids = None
        if groq_client and all_captions:
            arch_fig_ids = identify_architecture_figures_groq(groq_client, all_captions)
        
        if arch_fig_ids is None:
            arch_fig_ids = identify_architecture_figures_heuristic(caption_blocks)
            
        print(f"  Identified potential architecture figures: {arch_fig_ids}")
        
        diagram_count = 0
        for cap_data in caption_blocks:
            if cap_data['id'] not in arch_fig_ids:
                continue
                
            page_num = cap_data['page_num']
            page = doc[page_num]
            blocks = page.get_text("blocks")
            caption_rect = cap_data['rect']
            page_width = page.rect.width
            
            col_x0, col_x1 = get_column_bounds(caption_rect, page_width)
            y_top = 0
            y_bottom = page.rect.height
            
            # Find semantic bounds based on body text and other captions
            for b in blocks:
                if b[6] != 0 or b == cap_data['block_tuple']: 
                    continue
                b_rect = fitz.Rect(b[:4])
                b_text = b[4].strip()
                b_col_x0, b_col_x1 = get_column_bounds(b_rect, page_width)
                
                if not cols_overlap(col_x0, col_x1, b_col_x0, b_col_x1):
                    continue
                
                is_body = is_body_text(b_text)
                is_other_caption = bool(re.match(r'^(?:Figure|Fig\.|Table|Tab\.)\s*\d+', b_text, re.IGNORECASE))
                
                if is_body or is_other_caption:
                    if b_rect.y1 <= caption_rect.y0 + 5:
                        y_top = max(y_top, b_rect.y1)
                    elif b_rect.y0 >= caption_rect.y1 - 5:
                        y_bottom = min(y_bottom, b_rect.y0)
            
            fig_region = fitz.Rect(col_x0, y_top, col_x1, y_bottom)
            tight_rect = fitz.Rect(caption_rect)
            
            for img in page.get_image_info():
                img_rect = fitz.Rect(img["bbox"])
                if not (img_rect & fig_region).is_empty and rect_area(img_rect) < rect_area(page.rect) * 0.9:
                    tight_rect |= img_rect
                    
            for path in page.get_drawings():
                path_rect = fitz.Rect(path["rect"])
                if not (path_rect & fig_region).is_empty:
                    tight_rect |= path_rect
                    
            for b in blocks:
                if b[6] != 0 or b == cap_data['block_tuple']:
                    continue
                b_rect = fitz.Rect(b[:4])
                b_text = b[4].strip()
                if not is_body_text(b_text) and not bool(re.match(r'^(?:Figure|Fig\.|Table|Tab\.)\s*\d+', b_text, re.IGNORECASE)):
                    intersect = b_rect & fig_region
                    if not intersect.is_empty and rect_area(intersect) > 0.5 * rect_area(b_rect):
                        tight_rect |= b_rect
            
            if rect_area(tight_rect) < rect_area(caption_rect) * 1.5:
                tight_rect = fig_region
                
            # Add padding
            pad = 10
            tight_rect.x0 = max(0, tight_rect.x0 - pad)
            tight_rect.y0 = max(0, tight_rect.y0 - pad)
            tight_rect.x1 = min(page_width, tight_rect.x1 + pad)
            tight_rect.y1 = min(page.rect.height, tight_rect.y1 + pad)
            
            if (tight_rect.y1 - tight_rect.y0) < 50:
                continue
                
            try:
                pix = page.get_pixmap(clip=tight_rect, dpi=300)
                image = Image.open(io.BytesIO(pix.tobytes("png")))
                
                is_valid = True
                if or_client:
                    print(f"  Verifying {cap_data['id']} with OpenRouter Vision API...")
                    is_valid = is_architecture_diagram_openrouter(or_client, image)
                    time.sleep(1)
                    
                if is_valid:
                    diagram_count += 1
                    out_name = f"{paper_name}_arch_{diagram_count}.png"
                    out_path = os.path.join(output_dir, out_name)
                    image.save(out_path, "PNG")
                    print(f"  -> Successfully extracted: {out_name}")
                else:
                    print(f"  -> OpenRouter rejected {cap_data['id']} as it is not a valid diagram.")
            except Exception as e:
                print(f"  Error rendering {cap_data['id']}: {e}")
                
    print("Extraction complete.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    PDF_DIR = os.path.join(script_dir, "papers")
    OUT_DIR = os.path.join(script_dir, "architecture_diagrams")
    extract_architecture_diagrams(PDF_DIR, OUT_DIR)