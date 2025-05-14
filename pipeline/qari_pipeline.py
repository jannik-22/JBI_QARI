# pipeline/qari_pipeline.py

import os
from pathlib import Path
from typing import List
from tqdm import tqdm

import fitz
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from schema import JBIEntry

# Load environment
load_dotenv()

# Initialize LLM and parser
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
parser = PydanticOutputParser(pydantic_object=JBIEntry)

# Prompt template
prompt = PromptTemplate(
    template="""
You are a scientific analyst. Analyze the following academic paper text and extract information according to the JBI QARI Framework.

{format_instructions}

Text:
{input_text}
""",
    input_variables=["input_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Build processing chain
chain = prompt | llm | parser

def extract_text_from_pdf(pdf_path: Path) -> str:
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)

def run_qari_pipeline(input_dir: Path) -> List[dict]:
    entries = []
    pdf_files = list(input_dir.glob("*.pdf"))

    print(f"{len(pdf_files)} PDF files found.")

    for i, pdf_file in enumerate(tqdm(pdf_files, desc="📘 Running QARI analysis", unit="PDF"), start=1):
        tqdm.write(f"📄 Processing: {pdf_file.name}")
        try:
            text = extract_text_from_pdf(pdf_file)
            raw_result = chain.invoke({"input_text": text})

            result = raw_result if isinstance(raw_result, JBIEntry) else JBIEntry(**raw_result)
            result_dict = result.model_dump()
            result_dict["ID"] = i
            entries.append(result_dict)

        except Exception as e:
            tqdm.write(f"❌ Error with {pdf_file.name}: {e}")

    return entries
