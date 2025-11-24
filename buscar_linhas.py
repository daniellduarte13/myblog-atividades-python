import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")

s = requests.Session()
res = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)

# Busca linhas por termo (ex: "107", "800", "700")
termo = "107"
res = s.get(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={termo}"
)
linhas = res.json()

print(f"Linhas encontradas com termo '{termo}':")
for linha in linhas[:20]:  # Mostra as primeiras 20
    print(f"Código: {linha.get('cl', 'N/A')} - Nome: {linha.get('lt', 'N/A')} - Sentido: {linha.get('sl', 'N/A')}")

