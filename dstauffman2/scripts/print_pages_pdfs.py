# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 17:26:49 2018

@author: DStauffman
"""

#%% Imports
from PyPDF2 import PdfFileReader, PdfFileWriter

#%% Constants
src_file = r'C:\Users\DStauffman\Pictures\PDR TIM Receipts.pdf'
out_file = r'C:\Users\DStauffman\Pictures\PDR TIM - Avis Car Rental.pdf'
pages    = [0, ]

#%% Script
if __name__ == '__main__':
    # open the source file
    with open(src_file, 'rb') as file:
        # get reader and writers
        reader = PdfFileReader(file)
        writer = PdfFileWriter()
        # read each desired page and send it to the writer
        for page in pages:
            writer.addPage(reader.getPage(page))
        # write out the accumulated pages to disk
        with open(out_file, 'wb') as out:
            writer.write(out)
