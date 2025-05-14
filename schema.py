from pydantic import BaseModel, Field
from typing import Optional, List

# === JBI Entry purely descriptive ===
class JBIEntry(BaseModel):
    ID: Optional[int] = Field(None, description="Sequential number for internal tracking")
    Author: Optional[str] = Field(None, description="Name(s) of the author(s)")
    Title: Optional[str] = Field(None, description="Title of the paper")
    DOI: Optional[str] = Field(None, description="Digital Object Identifier")

    Methodology: Optional[str] = Field(None, description="Theoretical framework of the research (e.g., qualitative, quantitative)")
    Method: Optional[str] = Field(None, description="The way the data was collected (e.g., survey)")
    Phenomena_of_interest: Optional[str] = Field(None, description="Interventions or phenomena that researchers are focusing on")
    Setting: Optional[str] = Field(None, description="Specific setting of the research (e.g., online, hospital, etc.)")
    Geographical: Optional[str] = Field(None, description="General location of the research (e.g., country)")
    Cultural: Optional[str] = Field(None, description="Cultural characteristics (e.g., ethnic groups, socio-economic groups, etc.)")
    Participants: Optional[str] = Field(None, description="Number of participants and their characteristics such as age, gender, etc.")
    Data_analysis: Optional[str] = Field(None, description="Techniques used to analyze the data (e.g., Chi-Square Test, etc.)")
    Authors_conclusions: Optional[str] = Field(None, description="Study results as reported in the Findings Table")
    Reviewers_comments: Optional[str] = Field(None, description="Reviewer’s conclusions about the article’s findings")

# === Rating scheme with user-defined context ===
class Rating(BaseModel):
    relevance: int = Field(ge=0, le=4, description="To what extent is the content relevant to the analyzed topic?")
    transparency: int = Field(ge=0, le=4, description="How transparent and comprehensible is the methodological approach?")
    explanation: Optional[str] = Field(description="Free text: Why was this rating given?")

    @classmethod
    def scale(cls) -> dict[int, str]:
        return {
            0: "not fulfilled / inadequate",
            1: "slightly fulfilled",
            2: "partially fulfilled",
            3: "mostly fulfilled",
            4: "fully fulfilled"
        }

# === KeyFacts schema with user-defined context ===
class KeyFacts(BaseModel):
    key_statements: List[str]

    @classmethod
    def context(cls) -> str:
        return "Soft factors that influence non-conformities in quality management"
