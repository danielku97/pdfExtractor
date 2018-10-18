# pdfExtractor
Extracts text from a PDF by transforming pages into images, and using pytesseract as an OCR

This provides the base for transforming the PDF into images, which are converted to text.
Currently outputs a text dump of the PDFs, and requires regex to capture the data you want to find.
Comes with some useful functions such as reformatting phone numbers, removing ligatures, etc.

Instructions for use:
 - Import all necessary tools (Wand, Pillow, Pytesseract, Tesseract, etc.)
 - Create your own regex in the def extractData method
 
 When calling in the CLI, first argument is the PDF name in the same directory
 Eg. `python3 pdfExtract filename.pdf`

