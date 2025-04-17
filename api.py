from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import xml.etree.ElementTree as ET

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/lexml")
def consultar_lexml(termo: str = Query(..., description="Termo de busca, como 'artigo 5 da Constituição'")):
    url = f"https://www.lexml.gov.br/busca/sru?version=1.1&operation=searchRetrieve&query={termo}&maximumRecords=5"
    response = requests.get(url)

    if response.status_code != 200:
        return {"erro": "Falha ao consultar LexML"}

    root = ET.fromstring(response.content)
    resultados = []

    for record in root.findall(".//{http://www.loc.gov/zing/srw/}recordData"):
        titulo = record.find(".//{http://www.lexml.gov.br/schema/1.0/}titulo")
        link = record.find(".//{http://www.lexml.gov.br/schema/1.0/}link")

        resultados.append({
            "titulo": titulo.text if titulo is not None else "Sem título",
            "link": link.text if link is not None else "Sem link"
        })

    return {"resultados": resultados}
