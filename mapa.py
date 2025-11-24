from folium import Map, Marker
import requests
import os
import requests
from dotenv import load_dotenv

load_dotenv(".env")

s = requests.Session()
res = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"  # esse .env é para esconder o token da API (questão de segurança)
)
print(res.text)

res = s.get(
    "http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha=2506"
)
paradas = res.json()
paradas[:3]

m = Map(location=[paradas[3]["py"], paradas[3]["px"]], zoom_start=14)
for i in paradas:
    Marker(location=[i["py"], i["px"]], popup=i["np"]).add_to(m) # o popup de np é o Nome da Parada (quem diria kkkk)
m.show_in_browser()