# pipeline/keyfacts_pipeline.py

import os
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm
import fitz
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from schema import KeyFacts

# Load environment
load_dotenv()

# Initialize LLM and parser
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
parser = PydanticOutputParser(pydantic_object=KeyFacts)

# Get context from schema
context = KeyFacts.context()

# Prompt template
prompt = PromptTemplate(
    template=f"""
You are a scientific analyst.

Extract up to 5 key statements from the following academic text related to the topic: "{context}".
Make the statements concise, clear, and well-formulated.

Return only in the following JSON format:
{{format_instructions}}

Text:
{{input_text}}
""",
    input_variables=["input_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Build processing chain
chain = prompt | llm | parser


def extract_text_from_pdf(pdf_path: Path) -> str:
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)


def run_keyfacts_pipeline(input_dir: Path) -> List[Dict]:
    results: List[Dict] = []
    pdf_files = list(input_dir.glob("*.pdf"))
    print(f"{len(pdf_files)} PDF files found for key facts extraction.")

    for i, pdf in enumerate(
        tqdm(pdf_files, desc="📌 Extracting key facts", unit="PDF"), start=1
    ):
        tqdm.write(f"📄 Processing: {pdf.name}")
        try:
            text = extract_text_from_pdf(pdf)
            raw = chain.invoke({"input_text": text})
            facts = raw if isinstance(raw, KeyFacts) else KeyFacts(**raw)
            data = facts.model_dump()
            data["ID"] = i
            results.append(data)
        except Exception as e:
            tqdm.write(f"❌ Error with {pdf.name}: {e}")

    return results
