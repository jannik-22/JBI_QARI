import os
from pathlib import Path
from typing import List
from tqdm import tqdm

import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence

from schema import JBIEntry

# === Setup ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    temperature=0.0,
    model_name="gpt-4o-mini"
)

# === Output Parser & Prompt Setup ===
parser = PydanticOutputParser(pydantic_object=JBIEntry)

prompt = PromptTemplate(
    template="""
Du bist ein wissenschaftlicher Analyst. Analysiere den folgenden Text eines wissenschaftlichen Papers und extrahiere Informationen gemäß dem JBI QARI Framework.

{format_instructions}

Text:
{input_text}
""",
    input_variables=["input_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

# === PDF-Verarbeitung ===
def extract_text_from_pdf(pdf_path: Path) -> str:
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)

# === Hauptpipeline ===
def process_papers(input_dir: Path) -> List[JBIEntry]:
    entries = []
    pdf_files = list(input_dir.glob("*.pdf"))

    print(f"{len(pdf_files)} PDF-Dateien gefunden.")

    for i, pdf_file in enumerate(tqdm(pdf_files, desc="🔍 Verarbeite Paper", unit="PDF"), start=1):
        tqdm.write(f"📄 {pdf_file.name}")
        try:
            text = extract_text_from_pdf(pdf_file)
            raw_result = chain.invoke({"input_text": text})

            try:
                # Wenn chain korrektes Pydantic-Objekt liefert:
                if isinstance(raw_result, JBIEntry):
                    result = raw_result
                else:
                    # Versuch, dict in Pydantic-Modell zu verwandeln
                    result = JBIEntry(**raw_result)

                result_dict = result.model_dump()
                result_dict["ID"] = i
                entries.append(result_dict)

            except Exception as e:
                tqdm.write(f"❌ Fehler bei {pdf_file.name}: {e}")
        except Exception as e:
            tqdm.write(f"❌ Fehler bei {pdf_file.name}: {e}")

    return entries
