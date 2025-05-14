# pipeline/rating_pipeline.py

import os
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm
import fitz
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from schema import Rating

# Load environment variables (e.g., API keys)
load_dotenv()

# Initialize LLM and parser
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
parser = PydanticOutputParser(pydantic_object=Rating)

def build_prompt() -> str:
    # Build a block for each dimension showing its 0–4 descriptions
    scale_blocks = []
    for dimension, mapping in Rating.scale_descriptions().items():
        lines = [f"{dimension}:"]
        lines += [f"  {score}: {desc}" for score, desc in mapping.items()]
        scale_blocks.append("\n".join(lines))
    scale_text = "\n\n".join(scale_blocks)

    # List the field descriptions (excluding explanation)
    criteria_text = "\n".join(
        f"- {field.description}"
        for name, field in Rating.model_fields.items()
        if name != "explanation"
    )

    return f"""
You are a scientific analyst.

Evaluate the text according to the following criteria:
{criteria_text}

For each criterion, use the following 0–4 scale:
{scale_text}

Return the result **exclusively** in the following JSON format:
{{format_instructions}}

Text:
{{input_text}}
"""

# Create prompt template and chain
prompt = PromptTemplate(
    template=build_prompt(),
    input_variables=["input_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
chain = prompt | llm | parser

def extract_text_from_pdf(pdf_path: Path) -> str:
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)

def run_rating_pipeline(input_dir: Path) -> List[Dict]:
    results: List[Dict] = []
    pdf_files = list(input_dir.glob("*.pdf"))
    print(f"{len(pdf_files)} PDF files found for rating.")

    for i, pdf in enumerate(
        tqdm(pdf_files, desc="📊 Running rating analysis", unit="PDF"), start=1
    ):
        tqdm.write(f"📄 Processing: {pdf.name}")
        try:
            text = extract_text_from_pdf(pdf)
            raw = chain.invoke({"input_text": text})
            score = raw if isinstance(raw, Rating) else Rating(**raw)
            data = score.model_dump()
            data["ID"] = i
            results.append(data)
        except Exception as e:
            tqdm.write(f"❌ Error with {pdf.name}: {e}")

    return results
