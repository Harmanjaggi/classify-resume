from PyPDF2 import PdfReader
import pandas as pd
import numpy as np
import os
import re

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

dir_path = 'C:\interest\data_science\classify_resume\input1'
# dir_path = 'C:\interest\data_science\pdf_to_word\pdfs'

file_list = os.listdir(dir_path)
pdf_files = [file for file in file_list if file.lower().endswith('.pdf')]

pdf = []

for pdf_file in pdf_files:
    pdf_reader = PdfReader(dir_path + "\\" + pdf_file)
    pdf.append(pdf_reader)
    
len_of_pdf =  len(pdf)

pdfs = []

for i in range(len_of_pdf):
    pages = str()
    len_pages = len(pdf[i].pages)
    for j in range(len_pages):
        page = pdf[i].pages[0]
        # extracting page
        text = page.extract_text()
        pages += text
    # removing grammer
    new_text = re.sub(r"[^a-zA-Z0-9]", " ", pages.lower()).split()

    # remove stopwords
    filtered_sentence = [w for w in new_text if not w.lower() in stop_words]
    pdfs.append(filtered_sentence)
    
    
wordset = str()

for i in range(len_of_pdf):
    wordset = np.union1d(wordset,pdfs[i])

# Calculating Bag-of-Words

def calculateBOW(wordset,l_doc):
  tf_diz = dict.fromkeys(wordset,0)
  for word in l_doc:
      tf_diz[word]=l_doc.count(word)
  return tf_diz

    
df = pd.DataFrame()
for i in range(len_of_pdf): 
    bow = calculateBOW(wordset,pdfs[i])
    df["pdf " + str(i)] = bow
    
df2 = df[(df != 0).all(axis=1)]

df2.to_csv('output/resume_without_0.csv')

df3 = pd.read_csv('output/resume_without_0.csv')

df3.rename(columns={df3.columns[0]: 'Words'}, inplace=True)

print(df3)

df3.to_csv('output/resume_without_0.csv')