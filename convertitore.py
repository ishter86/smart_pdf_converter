# -*- coding: utf-8 -*-

# Import delle librerie necessarie
import os
import sys
import glob
import fitz
from pdf2docx import Converter as PdfToDocxConverter
from pdf2image import convert_from_path
import pytesseract
from docx import Document
import csv

print("Lingue supportate: ita, eng, fra, deu, spa")
lingue_da_usare = input("Inserisci i codici delle lingue da usare, separati da '+': ") # es. ita+eng

print("--- AVVIO CONVERTITORE PDF INTELLIGENTE ---")

# --- 1. CONFIGURAZIONE DEI PERCORSI (Versione Finale) ---
if getattr(sys, 'frozen', False):
    # Se siamo un .exe "congelato", il percorso di sys.executable è dentro la cartella /dist/nomeprogramma
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))
else:
    # Se siamo uno script .py normale, il percorso base è la cartella dello script
    base_path = os.path.dirname(__file__)

# Definiamo i percorsi per le cartelle Input e Output partendo dal percorso base
input_dir = os.path.join(base_path, "In")
output_dir = os.path.join(base_path, "Out")

# Creiamo le cartelle se non esistono (questa parte è invariata)
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Configurazione Tesseract e Poppler (invariata, ma ora usa base_path)
poppler_path_relative = os.path.join(base_path, "dependencies", "poppler", "bin")
tesseract_path_relative = os.path.join(base_path, "dependencies", "tesseract", "tesseract.exe")

pytesseract.pytesseract.tesseract_cmd = tesseract_path_relative
print(f"I PDF verranno letti da: {input_dir}")
print(f"I risultati verranno salvati in: {output_dir}")

# --- 2. LOGICA PRINCIPALE ---

# --- MODIFICA 3: Modifichiamo il pattern di ricerca per puntare alla cartella Input ---
pdf_search_pattern = os.path.join(input_dir, "*.pdf")
file_pdf_da_processare = glob.glob(pdf_search_pattern)

report_dati = [["Nome File", "Conteggio Caratteri", "Metodo"]]

if not file_pdf_da_processare:
    print(f"\nATTENZIONE: Nessun file PDF trovato nella cartella '{input_dir}'.")
else:
    print(f"\nTrovati {len(file_pdf_da_processare)} file PDF da processare...")

for full_path_file in file_pdf_da_processare:
    nome_file = os.path.basename(full_path_file) # <-- MODIFICA: Estraiamo solo il nome del file dal percorso completo
    print(f"\n--- Sto processando: {nome_file} ---")
    
    # ... (La logica di estrazione testo e OCR rimane identica) ...
    testo_per_analisi = ""
    conteggio = 0
    metodo = ""

    try:
        with fitz.open(full_path_file) as doc:
            for pagina in doc:
                testo_per_analisi += pagina.get_text()
        conteggio = len(testo_per_analisi.strip())
    except Exception as e:
        print(f"ERRORE: Impossibile leggere il file PDF '{nome_file}'. Salto al prossimo. Dettagli: {e}")
        report_dati.append([nome_file, 0, "Errore di lettura"])
        continue

    # --- MODIFICA 4: Creiamo il percorso di output per il file Word ---
    nome_file_word_base = nome_file.replace(".pdf", ".docx")
    percorso_file_word_output = os.path.join(output_dir, nome_file_word_base)

    if conteggio > 150:
        metodo = "Conversione Diretta (pdf2docx)"
        print(f"Testo trovato ({conteggio} caratteri). Avvio conversione con formattazione...")
        try:
            cv = PdfToDocxConverter(full_path_file)
            cv.convert(percorso_file_word_output) # Salva nel percorso di output
            cv.close()
            print(f"File salvato come: {percorso_file_word_output}")
        except Exception as e:
            print(f"ERRORE durante la conversione con pdf2docx: {e}")
            metodo = "Errore Conversione Diretta"
            conteggio = -1
    else:
        metodo = "OCR (Tesseract)"
        print(f"Poco testo trovato ({conteggio} caratteri). Avvio OCR...")
        try:
            immagini_pdf = convert_from_path(full_path_file, poppler_path=poppler_path_relative)
            testo_ocr = ""
            for i, img in enumerate(immagini_pdf):
                print(f"  - Analisi OCR pagina {i + 1}/{len(immagini_pdf)}...")
                testo_ocr += pytesseract.image_to_string(img, lang=lingue_da_usare)
            
            conteggio = len(testo_ocr)
            
            documento_word = Document()
            documento_word.add_paragraph(testo_ocr)
            documento_word.save(percorso_file_word_output) # Salva nel percorso di output
            print(f"OCR completato. File salvato come: {percorso_file_word_output}")

        except Exception as e:
            print(f"ERRORE fatale durante l'OCR: {e}")
            metodo = "Errore OCR"
            conteggio = -1

    report_dati.append([nome_file, conteggio, metodo])
    print(f"Conteggio caratteri registrato: {conteggio}")

# --- 3. SCRITTURA DEL REPORT FINALE ---
# --- MODIFICA 5: Creiamo il percorso di output per il file CSV ---
percorso_report_output = os.path.join(output_dir, "report_conversione.csv")
try:
    with open(percorso_report_output, "w", newline="", encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv)
        writer.writerows(report_dati)
    print("\n--- RIEPILOGO SALVATO ---")
    print(f"Creato file di report in: '{percorso_report_output}'")
except Exception as e:
    print(f"\nERRORE: Impossibile scrivere il file di report: {e}")

print("\n--- TUTTO COMPLETATO! ---")
input("Premi INVIO per chiudere.")