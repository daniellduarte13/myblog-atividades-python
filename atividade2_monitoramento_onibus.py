import os
import argparse
import webbrowser
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

load_dotenv(".env")


def get_session():
    s = requests.Session()
    token = os.getenv("SPTRANS_TOKEN")
    if token:
        try:
            s.post(f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}", timeout=10)
        except Exception:
            pass
    return s


def criar_mapa(codigo_linha: str, session=None, save_html=True):
    if session is None:
        session = get_session()

    res_paradas = session.get(
        f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo_linha}", timeout=10
    )
    try:
        paradas = res_paradas.json()
    except Exception:
        paradas = []

    res_pos = session.get(
        f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={codigo_linha}", timeout=10
    )
    try:
        posicoes = res_pos.json()
    except Exception:
        posicoes = {}

    veiculos = posicoes.get("vs", []) if isinstance(posicoes, dict) else []

    if isinstance(paradas, list) and len(paradas) > 0:
        m = Map(location=[paradas[0]["py"], paradas[0]["px"]], zoom_start=14)
    elif veiculos and len(veiculos) > 0:
        m = Map(location=[veiculos[0]["py"], veiculos[0]["px"]], zoom_start=14)
    else:
        m = Map(location=[-23.5505, -46.6333], zoom_start=12)

    if isinstance(paradas, list):
        for p in paradas:
            Marker(
                location=[p.get("py"), p.get("px")],
                popup=p.get("np", "Parada"),
                icon=Icon(color="blue", icon="info-sign", prefix="glyphicon"),
            ).add_to(m)

    for v in veiculos:
        Marker(
            location=[v.get("py"), v.get("px")],
            popup=f"Ônibus {v.get('p', 'N/A')}",
            icon=Icon(color="red", icon="bus", prefix="fa"),
        ).add_to(m)

    filename = f"map_{codigo_linha}.html"
    if save_html:
        m.save(filename)
        webbrowser.open(os.path.abspath(filename))

    return m


def main():
    parser = argparse.ArgumentParser(description="Gerar mapa de paradas e posições em tempo real para uma linha")
    parser.add_argument("--codigo", help="Código da linha (ex: 2506)", default=os.getenv("SPTRANS_LINE", "1892"))
    args = parser.parse_args()

    session = get_session()
    criar_mapa(args.codigo, session=session, save_html=True)


if __name__ == "__main__":
    main()
