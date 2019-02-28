#!/bin/bash
./fetch.sh
python ./download_pdfs_asyn.py
python parse_pdf_to_text.py
python thumb_pdf.py
python analyze.py
python buildsvm.py
python make_cache.py

