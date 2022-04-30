import requests
import bs4
import tabulate

# Simulando um browser para que o servidor aceite a requisição
headers = {'User-Agent': 'Mozilla/5.0'}

# Solicitando requisição do servidor
resposta = requests.post('https://www.fundamentus.com.br/fii_resultado.php', headers=headers)

pass
