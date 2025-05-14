# 🧠 JBI QARI Analysis Pipeline

Automated analysis of scientific PDFs using the JBI QARI framework, powered by OpenAI and LangChain.

## ⚙️ Features
   ✅ PDF processing via PyMuPDF

   🤖 LLM-based evaluation via OpenAI API (LangChain)

   📊 Structured multi-sheet Excel output

   🔄 Real-time progress display with tqdm

   🧩 Modular support for:

      JBI QARI extraction
      Rating scoring
      Key Facts extraction

## 🚀 Usage
1. Set your OpenAI API key in a .env file:
   ```
   OPENAI_API_KEY=sk-...
   ```

2. Place your PDF files inside the input/ folder (Create the required folders [/input and /output in the root directory]).

3. Customize schema.py if needed (e.g., modify data fields or descriptions):
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

4. Run the pipeline:
   ```
   python main.py
   ```

## 📁 Output
Results will be saved to:
```
output/analyse_ergebnisse.xlsx
```

## 🧩 Dependencies
Install required packages with:
```
pip install -r requirements.txt
```