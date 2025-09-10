# Convertitore PDF Intelligente v1.0

Uno strumento da riga di comando per convertire file PDF in documenti Word (.docx), con supporto OCR per i file scansionati. Lo strumento offre anche il conteggio caratteri.

## Come Usarlo

Ci sono due modi per usare questo programma:

### 1. Per Utenti Finali (Uso Semplice)
Se vuoi solo usare il programma senza installare Python, puoi scaricare il pacchetto "chiavi in mano" per Windows.
1.  Vai alla sezione **[Releases](https://github.com/ishter86/smart_pdf_converter/releases)** di questo progetto.
2.  Scarica il file `.zip` dall'ultima release (es. `ConvertitorePDF_v1.0.zip`).
3.  Estrai tutto il contenuto dello zip in una cartella.
4.  Metti i file PDF che vuoi convertire nella sottocartella `In`.
5.  Fai doppio clic su `convertitore.cmd`.
6.  Trova i file convertiti e il report nella cartella `Out`.

### 2. Per Sviluppatori (Eseguire da Codice Sorgente)

**Prerequisiti:**
- Python 3.8+
- Tesseract OCR
- Poppler

**Installazione:**
1.  Clona il repository: `git clone https://github.com/ishter86/smart_pdf_converter.git`
2.  Naviga nella cartella: `cd NOME_REPOSITORY`
3.  Installa le dipendenze Python: `pip install -r requirements.txt`

**Utilizzo:**
1.  Metti i file PDF nella cartella `Input`.
2.  Esegui lo script: `python convertitore.py`
3.  I risultati verranno salvati nella cartella `Output`.
