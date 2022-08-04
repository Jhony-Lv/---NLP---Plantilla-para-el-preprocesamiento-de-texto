import numpy as np
import pandas as pd
import re  
import xlrd 
import nltk
import json
from tqdm import tqdm
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import random



#Cargamos el dataset
df = pd.read_excel( ) 
df.columns.tolist()

#Realizamos la limpieza del texto
datos_pre = []

for i in tqdm( range(0, len(df)) ):
    texto = re.sub(r"""[!¡?':"-.áéíóú<>(){}@%&*/[/]""", func_remplazo, df[][i])
    texto = texto.lower()
    texto = texto.split()
    ps = PorterStemmer()
    texto = [ps.stem(word) for word in texto if not word in set(stopwords.words('spanish'))]
    texto = [correction(word) for word in texto]
    texto = ' '.join(texto)
    datos_pre.append(texto) 


#print("no" in pal)

#Guardamos los datos preprocesados
with open('datos_pre.txt', 'w', encoding='latin1') as filehandle:
    json.dump(datos_pre, filehandle)

#----------Función para sustitir las palabras con tilde
def func_remplazo(match):
    if(match[0] == "á"):
        return "a"
    elif(match[0] == "é"):
        return "e"
    elif(match[0] == "í"):
        return "i"
    elif(match[0] == "ó"):
        return "o"
    elif(match[0] == "ú"):
        return "u"    
    else:
        return " "


#Funciones para la corrección de palabras
def words(text): 
    return re.findall(r'\w+', text.lower())


WORDS = Counter(words(open('diccionario.txt', encoding='utf-8').read()))


def P(word, N=sum(WORDS.values())): 
    
    return WORDS[word] / N

def correction(word): 
    return max(candidates(word), key=P)

def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    return set(w for w in words if w in WORDS)

def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
