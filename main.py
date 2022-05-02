import requests
from bs4 import BeautifulSoup
import tabulate

# Simulando um browser para que o servidor aceite a requisição
headers = {'User-Agent': 'Mozilla/5.0'}

# Solicitando requisição do servidor
resposta = requests.post('https://www.fundamentus.com.br/fii_resultado.php', headers=headers)

# Criado um novo objeto que retorna uma estrutura de dados aninhados
soup = BeautifulSoup(resposta.text, 'html.parser')

# Buscando todas as linhas da tabela de fundos imobiliários
linhas = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

# Utilizando o laço for para iterar sobre as linhas encontradas
for linha in linhas:

    # Encontrando todas as linhas que possuem
    # Os dados necessários das FII
    dados_fundo = linha.find_all('td')

    # Mostrando os dados na tela utilizando o índice
    print(dados_fundo[0].text)
