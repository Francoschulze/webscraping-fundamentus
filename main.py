import requests
from bs4 import BeautifulSoup
import locale
from tabulate import tabulate

from modelos import FundoImobiliario, Estrategia

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def trata_porcentagem(porcentagem_str):
    return locale.atof(porcentagem_str.split('%')[0])


def trata_decimal(decimal_str):
    return locale.atof(decimal_str)


# Simulando um browser para que o servidor aceite a requisição
headers = {'User-Agent': 'Mozilla/5.0'}

# Solicitando requisição do servidor
resposta = requests.post('https://www.fundamentus.com.br/fii_resultado.php', headers=headers)

# Criado um novo objeto que retorna uma estrutura de dados aninhados
soup = BeautifulSoup(resposta.text, 'html.parser')

# Buscando todas as linhas da tabela de fundos imobiliários
linhas = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

resultado = []

# Definindo os parâmetros para um exemplo de filtro
# para a nossa estratégia
estrategia = Estrategia(
    cotacao_atual_minima=50.0,
    dividend_yield_minimo=5,
    p_vp_minimo=0.70,
    valor_mercado_minimo=200000000,
    liquidez_minima=50000,
    qt_minima_imoveis=5,
    maxima_vacancia_media=10
)

# Utilizando o laço for para iterar sobre as linhas encontradas
for linha in linhas:
    dados_fundo = linha.find_all('td')
    codigo = dados_fundo[0].text
    segmento = dados_fundo[1].text
    cotacao = trata_decimal(dados_fundo[2].text)
    ffo_yield = trata_porcentagem(dados_fundo[3].text)
    dividend_yield = trata_porcentagem(dados_fundo[4].text)
    p_vp = trata_decimal(dados_fundo[5].text)
    valor_mercado = trata_decimal(dados_fundo[6].text)
    liquidez = trata_decimal(dados_fundo[7].text)
    qt_imoveis = int(dados_fundo[8].text)
    preco_m2 = trata_decimal(dados_fundo[9].text)
    aluguel_m2 = trata_decimal(dados_fundo[10].text)
    cap_rate = trata_porcentagem(dados_fundo[11].text)
    vacancia = trata_porcentagem(dados_fundo[12].text)

    fundo_imobiliario = FundoImobiliario(
        codigo, segmento, cotacao, ffo_yield, dividend_yield, p_vp, valor_mercado,
        liquidez, qt_imoveis, preco_m2, aluguel_m2, cap_rate, vacancia
        )
    # Adicionando na lista resultado os valores retornados como True
    if estrategia.aplica_estrategia(fundo_imobiliario):
        resultado.append(fundo_imobiliario)

# Cabeçalho para o uso da tabulate
cabecalho = ['ÍNDICE', 'CÓDIGO', 'SEGMENTO', 'COTAÇÃO ATUAL', 'DIVIDEND YIELD']

tabela = []

for elemento in resultado:
    tabela.append([
        elemento.codigo,
        elemento.segmento,
        locale.currency(elemento.cotacao_atual),
        f'{locale.str(elemento.dividend_yield)} %'
    ])

print(tabulate(tabela, headers=cabecalho, showindex='always', tablefmt='fancy_grid'))

