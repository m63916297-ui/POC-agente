# Librería de LLM
from groq import Groq

# Librerías de manejo de texto
import re
import string

# Manejo de datos
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool

from vector_search import *

# Crear el cliente Groq que permite enviar peticiones al modelo Llama-3.1-8b-instant.
client_groq = Groq(api_key=os.getenv('ClientGroq'))


################################################################
# Limpiar y normalizar las respuestas o entradas del LLM para análisis y visualización.
################################################################
def limpiar_texto(texto: str) -> str:
    """
    Función para limpiar el texto:
      Eliminar signos de puntuación
      Eliminar caracteres especiales
      Eliminar espacios extra
    :param texto: Texto a limpiar.
    :return: Texto limpio.
    """

    # Eliminar signos de puntuación y frase común
    texto = re.sub(f"[{re.escape(string.punctuation)}]", "", texto)
    texto = texto.replace("La categoría más acorde al texto es ","")
    texto = texto.capitalize()

    # Eliminar caracteres especiales
    texto = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]', '', texto)
    # 4. Eliminar espacios extra
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto

################################################################
# Clasificar un texto en una de las categorías dadas usando un modelo LLM.
################################################################
def Clasificar(texto):
  """
  Función para identificar el número de cedula.
  :param texto: Texto a revisar.
  """
  try:
    llm = client_groq.chat.completions.create(model="llama-3.1-8b-instant",
                                              messages=[{"role":"system","content":f"""Eres un agente encargado de identificar documentos de identidad dentro de un conversación
                                                         Devuelve el número de documento completo.
                                                         """},
                                              {"role":"user","content":texto}],
                                              temperature=0.2,
                                              max_tokens=250)

    return limpiar_texto(llm.choices[0].message.content)
  except:
    return "Error"

################################################################  
# Mapa básico de números escritos en español a su valor numérico
################################################################
MAPA_NUMEROS = {
    "cero": 0, "uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4,
    "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
    "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14,
    "quince": 15, "dieciséis": 16, "dieciseis": 16, "diecisiete": 17,
    "dieciocho": 18, "diecinueve": 19, "veinte": 20, "treinta": 30,
    "cuarenta": 40, "cincuenta": 50, "sesenta": 60, "setenta": 70,
    "ochenta": 80, "noventa": 90, "cien": 100, "ciento": 100,
    "doscientos": 200, "trescientos": 300, "cuatrocientos": 400,
    "quinientos": 500, "seiscientos": 600, "setecientos": 700,
    "ochocientos": 800, "novecientos": 900, "mil": 1000
}


def texto_a_numero(palabra):
    """Convierte una palabra numérica simple a su valor numérico (si existe)."""
    return MAPA_NUMEROS.get(palabra.lower())


def extraer_numeros(texto):
    """
    Extrae todos los números de un texto, incluyendo los escritos como palabra.
    Devuelve una lista de números enteros.
    """
    texto = texto.lower()
    numeros = []

    # Extraer números escritos en dígito
    for n in re.findall(r"\b\d+\b", texto):
        numeros.append(int(n))

    # Extraer números escritos en palabras (simples)
    palabras = re.findall(r"\b[a-záéíóúñ]+\b", texto)
    for p in palabras:
        num = texto_a_numero(p)
        if num is not None:
            numeros.append(num)
    print(numeros)
    return int("".join(map(str, numeros)))

def search_identification(cedula):
    df  = pd.read_excel('cesancias_causadas.xlsx')

    # Filtrar el DataFrame
    df = df[df.iloc[:, 0] == cedula]

    # Tomar la primera fila del filtro y obtener la segunda y tercera columnas
    if not df.empty:
        fila = df.iloc[0]  
        valor = fila.iloc[1]   
        mes = fila.iloc[2].month 
        anio = fila.iloc[2].year 
        return f"La cedula {cedula} tiene ${valor} en el mes {(mes)} del año {anio}"
    else:
        return f" Cedula {cedula} no se encontró"


@tool
def validardoc(numero_documento):
    """
    Identificar los números de documento y validar la información dentro de la base de excel
    numero_documento: número de documento brindado por el usuario
    """
    print('##### Se está haciendo la validación de la cedula ###')
    try:
        numdoc = Clasificar(numero_documento)
        
        numdoc = limpiar_texto(numdoc)
        numdoc = extraer_numeros(numdoc)
        numdoc= search_identification(numdoc)

        return numdoc
    except Exception as e:
        print(f"Error al obtener el número {numero_documento}: {e}")
        return f"No se pudo obtener información del documento {numero_documento}"
   
def retreival_RAG(solicitudususario):
    # Cargar base vectorial persistente
    index_path = "vector_db/cesantias.index"
    metadata_path = "vector_db/cesantias_meta.json"

    index, metadata = load_vector_store(index_path, metadata_path)

    # Realizar consulta
    resultados = search_similar(solicitudususario, index, metadata, k=10)

    return resultados