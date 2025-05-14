from pathlib import Path

from pipeline.qari_pipeline import run_qari_pipeline
from pipeline.rating_pipeline import run_rating_pipeline
from pipeline.keyfacts_pipeline import run_keyfacts_pipeline

from utils import save_multi_sheet_excel

# === Control: What should run? ===
RUN_QARI = True
RUN_RATING = True
RUN_KEYFACTS = True

# === Paths ===
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COMBINED_FILE = OUTPUT_DIR / "analysis_results.xlsx"

def main():
    combined_data = {}

    if RUN_QARI:
        print("\nStarting JBI QARI analysis...")
        qari_results = run_qari_pipeline(INPUT_DIR)
        if qari_results:
            combined_data["JBI QARI"] = qari_results
        else:
            print("⚠️ No JBI QARI data extracted.")

    if RUN_RATING:
        print("\nStarting rating analysis...")
        rating_results = run_rating_pipeline(INPUT_DIR)
        if rating_results:
            combined_data["Rating"] = rating_results
        else:
            print("⚠️ No rating data extracted.")

    if RUN_KEYFACTS:
        print("\nStarting key facts extraction...")
        keyfacts_results = run_keyfacts_pipeline(INPUT_DIR)
        if keyfacts_results:
            combined_data["KeyFacts"] = keyfacts_results
        else:
            print("⚠️ No key facts extracted.")

    if combined_data:
        save_multi_sheet_excel(combined_data, COMBINED_FILE)
        print(f"\nAll results saved in: {COMBINED_FILE}")

if __name__ == "__main__":
    main()
