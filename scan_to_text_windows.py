#import area - start
import tkinter # Module for file selecting window
from tkinter import filedialog, messagebox
from PyPDF2 import PdfFileReader, PdfFileWriter
from docx.opc.oxml import parse_xml # Module to merge PDFs

from pdf2image import convert_from_path # Module to convert .pdf to .png

import cv2 # Module for image processing. This helps for better "reading" of the picture
import pytesseract # Module for extracting the text of an image. Has to be installed with "pip" and "path" and ".exe" on Windows systems! See on githup of "tesseract". 

from docx import Document

from deep_translator import GoogleTranslator
#import area - end

#function area - start
def valid_xml_char_ordinal(c): # Function to convert turkish characters to xml chars
    codepoint = ord(c)
    return ( # conditions ordered by presumed frequency
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
    )                            
#function area - end


#code - start

#Merge scanned PDFs to only one file.
root = tkinter.Tk() # The actuall dialog window, witch has to be defined as "parent" with the askopenfilenames() function
root.withdraw() # To get rid of the small TK window
files = filedialog.askopenfilenames(parent=root, title='Select the PDFs to be merged!') # This function saves the paths of the files in a coventional python list

# Get every selected pdf an convert it to png
pdf_counter= 1 # Counter for the naming of the .png files for every PDF file
doc = Document() # Opens a new Word-File. It hads to be opend before the loops to prevent overriding the existing file
poppler = r'C:\Users\windows\Downloads\poppler-0.68.0\bin'

#Information windwos "Please wait..."
root.after(7000, root.destroy) #Closes window after 7 seconds. 
tkinter.messagebox.showinfo(title='Information', message='Please wait until the PDFs are converted! This window closes in 7 seconds...')

for file in root.tk.splitlist(files): # This loop goes through every pdf file which were selected in the file dialog
    
    png_files = convert_from_path(file, dpi=300, poppler_path=poppler) # Get the path of every file and safe it in a variable
     
    # Save every pdf as png 
    for png_file in png_files:
        name = str(pdf_counter) + 'out.png' # Naming of the .png files
        png_file.save(name, 'PNG') # Saving the converted .png file
        

        # Get text of every png
        for img in png_files:
            #name = str(img) + 'out.png' # To get evey pictures name, which we named while converting from .pdf to .png
            pic_texts = cv2.imread(name)
            pytesseract.pytesseract.tesseract_cmd = r'C:\Users\windows\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(pic_texts, lang="tur")

            #Translate text from Turkish to German 
            translated = GoogleTranslator(source='turkish', target='german').translate(text)

            #Write text direcly to a Word file
            cleaned_string = ''.join(c for c in translated if valid_xml_char_ordinal(c)) # Replace chars with XML counterparts
            
            #print(cleaned_string)
            doc.add_paragraph(cleaned_string) # Writes the content in the variable into the .docx file 
            doc.add_page_break()
            doc.save('sohbet.docx')     
           
            pdf_counter+= 1 # Increase the counter for a new unique name

root.after(7000, root.destroy) #Closes window after 7 seconds. 
tkinter.messagebox.showinfo(title='Finished', message='Converting is done! This window closes in 7 seconds...')
