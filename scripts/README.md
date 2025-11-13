# Scripts Directory

This directory contains development scripts and source materials that are not needed for the live website.

## Files

### Python Scripts

- **`generate_audio.py`** - Generates MP3 audio files for all spelling words using Google Cloud Text-to-Speech API
  - Usage: `python generate_audio.py --voice-type female --grade-level both`
  - Requires: Google Cloud credentials set in `GOOGLE_APPLICATION_CREDENTIALS` environment variable
  - Output: Creates MP3 files in `../audio/gr23/` and `../audio/gr45/`

- **`extract_pdf.py`** - Extracts text from PDF spelling lists
  - Usage: `python extract_pdf.py "spelling-2026-gr45-list.pdf"`
  - Used during initial setup to extract word lists from PDFs

### Dependencies

- **`requirements.txt`** - Python package dependencies
  - PyPDF2>=3.0.0
  - google-cloud-texttospeech>=2.14.0
  - Install with: `uv pip install -r requirements.txt` (in virtual environment)

### Source PDFs

- **`spelling-2026-gr23-list.pdf`** - PSIA spelling list for Grades 2-3 (600 words)
- **`spelling-2026-gr45-list.pdf`** - PSIA spelling list for Grades 4-5 (800 words)

## Setup Notes

The audio files have already been generated and are stored in the `audio/` directory. These scripts are kept for reference and in case you need to regenerate the audio files in the future (e.g., using a different voice or if new words are added).

## Regenerating Audio Files

If you need to regenerate the audio files:

1. Set up Google Cloud credentials (see main README for instructions)
2. Activate virtual environment: `source ../.venv/bin/activate`
3. Run: `python generate_audio.py --voice-type female --grade-level both`

The script will generate approximately 1,400 MP3 files (600 for gr2-3, 800 for gr4-5).
