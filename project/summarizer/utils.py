import PyPDF2
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client for laozhang.ai
client = OpenAI(
    api_key=os.getenv("LAOZHANG_API_KEY"),
    base_url="https://api.laozhang.ai/v1"
)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            return text if text else "No text could be extracted from the PDF."
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def summarize_text(text):
    """Summarize text using laozhang.ai's Grok API."""
    try:
        response = client.chat.completions.create(
            model="grok-3",  # Use "grok-beta" if grok-3 is unavailable
            messages=[
                {"role": "system", "content": "You are a helpful AI that summarizes text concisely and accurately."},
                {"role": "user", "content": f"Summarize this text in 200 words or less: {text}"}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing text: {str(e)}"