import calendar
from datetime import datetime, timedelta
import plotly.graph_objects as go
import requests

BASE_URL = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
    "?@dataInicial='{date}'&@dataFinalCotacao='{date}'&$format=json"
)

def get_cotacao(data):
    data_formatada = data.strftime("%m-%d-%Y")
    url = BASE_URL.format(date=data_formatada)
    res = requests.get(url, timeout=10).json()
    valores = res.get("value") or []
    return valores[0]["cotacaoVenda"] if valores else None

def buscar_cotacao_dia_anterior(data):
    dia_anterior = data - timedelta(days=1)
    cotacao = get_cotacao(dia_anterior)
    if cotacao is not None:
        return cotacao
    return buscar_cotacao_dia_anterior(dia_anterior)

def cotacao_dolar_periodo(mmyyyy):
    first_date = datetime.strptime(mmyyyy, "%m%Y")
    last_date = first_date.replace(
        day=calendar.monthrange(first_date.year, first_date.month)[1]
    )
    datas = []
    cotacoes = []

    data_atual = first_date
    while data_atual <= last_date:
        cotacao = get_cotacao(data_atual)
        if cotacao is None:
            cotacao = buscar_cotacao_dia_anterior(data_atual)
        datas.append(data_atual)
        cotacoes.append(cotacao)
        data_atual += timedelta(days=1)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=datas,
            y=cotacoes,
            mode="lines+markers",
            name="Cotação do Dólar",
        )
    )

    fig.update_layout(
        title=f'Cotação do Dólar - {first_date.strftime("%m/%Y")}',
        xaxis_title="Data",
        yaxis_title="Cotação (R$)",
    )

    return fig

grafico = cotacao_dolar_periodo("042011")
grafico.show()
