# 🧠 JBI QARI Analysepipeline

Automatisierte Analyse wissenschaftlicher PDFs nach dem JBI QARI Framework mit Hilfe von OpenAI & LangChain.

## ⚙️ Features
- PDF-Verarbeitung mit PyMuPDF
- LLM-Auswertung via OpenAI API (LangChain)
- Strukturierte Ausgabe in Excel
- Fortschrittsanzeige mit tqdm

## 🚀 Nutzung
1. OpenAI API-Key in `.env` setzen:
   ```
   OPENAI_API_KEY=sk-...
   ```
2. PDFs in `input/` ablegen

3. Schema.py öffnen und eventuelle Anpassungen durchführen!
```
class JBIEntry(BaseModel):
    ID: Optional[int] = Field(None, description="Laufende Nummer für interne Zuordnung")
    Author: Optional[str] = Field(None, description="Name(n) des Autors oder der Autoren")
    Title: Optional[str] = Field(None, description="Titel des Papers")
    DOI: Optional[str] = Field(None, description="Digital Object Identifier")

    Methodology: Optional[str] = Field(None, description="Theoretical framework of the research (e.g., qualitative, quantitative)")
    Method: Optional[str] = Field(None, description="The way the data was collected (e.g., survey)")
    Phenomena_of_interest: Optional[str] = Field(None, description="Interventions or occurrences that researchers focus on")
    Setting: Optional[str] = Field(None, description="Specific location of the research (e.g., online, hospital, etc.)")
    Geographical: Optional[str] = Field(None, description="General location of the research (e.g., country)")
    Cultural: Optional[str] = Field(None, description="Cultural features (e.g., ethnic groups, socio-economic groups, etc.)")
    Participants: Optional[str] = Field(None, description="Number of participants, and their age, gender, etc.")
    Data_analysis: Optional[str] = Field(None, description="Techniques used to analyse data (e.g., Chi-Squared Test, etc.)")
    Authors_conclusions: Optional[str] = Field(None, description="Study results reported in the Findings Table")
    Reviewers_comments: Optional[str] = Field(None, description="Reviewer’s conclusions regarding the findings of the article")
```

4. Pipeline starten:
   ```
   python main.py
   ```

## 📁 Output
Die Datei `output/jbi_results.xlsx` enthält strukturierte Ergebnisse (u.a. Autor, Methode, Setting, etc.).

## 🧩 Abhängigkeiten
Installierbar mit:
```
pip install -r requirements.txt
```
Benötigte Pakete: `langchain`, `openai`, `pydantic`, `python-dotenv`, `fitz` (PyMuPDF), `tqdm`, `pandas`, `openpyxl`