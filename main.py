from pathlib import Path
from pipeline import process_papers
from utils import save_results_to_excel

# === Pfade definieren ===
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "jbi_results.xlsx"

def main():
    print("📄 Starte JBI QARI Analysepipeline...")

    # Sicherstellen, dass der Output-Ordner existiert
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # PDFs verarbeiten
    entries = process_papers(INPUT_DIR)

    if not entries:
        print("⚠️ Keine Einträge extrahiert.")
        return

    # In Excel speichern
    save_results_to_excel(entries, OUTPUT_FILE)
    print(f"✅ Ergebnisse gespeichert in: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
