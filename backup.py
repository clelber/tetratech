#importação do chrome para controle do navegador
from selenium.webdriver import Chrome
import time as t
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json


navegador = Chrome("chromedriver")
navegador.get("http://www.bibliotecavirtual.sp.gov.br/temas/sao-paulo/sao-paulo-populacao-do-estado.php")
navegador.maximize_window()
t.sleep(3)
linhas = navegador.find_elements_by_xpath("/html/body/div[3]/div/div[1]/article/div/div")

lista = []
for linha in linhas:
    tds = linha.find_elements_by_tag_name('td')
    for i, t in enumerate(tds, 1):
        lista.append(t.text)
print(lista)


ufs = {"AC": "Acre", "AL": "Alagoas", "AM": "Amazonas", "AP": "Amapá", "BA": "Bahia", "CE": "Ceará",
       "DF": "Distrito Federal", "ES": "Espirito Santo", "GO": "Goiás", "MA": "Maranhão", "MG": "Minas Gerais",
       "MS": "Mato Grosso do Sul", "MT": "Mato Grosso", "PA": "Pará", "PB": "Paraiba", "PE": "Pernambuco",
       "PI": "Piauí", "PR": "Paraná", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RO": "Rondônia",
       "RR": "Roraima", "RS": "Rio Grande do Sul", "SC": "Santa Catarina", "SE": "Sergipe", "SP": "São Paulo",
       "TO": "Tocantins"}

for uf in ufs:
    url = f'https://s3-sa-east-1.amazonaws.com/ckan.saude.gov.br/PNI/vacina/uf/2021-07-06/uf%3D{uf}/'\
          f'part-00000-2266a6be-a6af-4755-86bc-9c3b75d8f506.c000.csv'

    df = pd.read_csv(url, encoding='cp1252', skiprows=1, sep=';', low_memory=False)
    vacinados = len(df.index)
    populacao = ''
    for index, linha in enumerate(lista):
        if ufs[uf] in linha:
            populacao = lista[index+1]
            populacao = str(populacao).replace('.', '')
            break

    aderencia = (100 * vacinados) / int(populacao)
    fig, ax = plt.subplots(1, 1)

    data = [[ufs[uf], populacao, f'{vacinados:,.2f}', '{:.2f}'.format(aderencia)]]

    column_labels = ["Unidade Federativa", "População", "Vacinados", "Aderência (%)"]
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data, colLabels=column_labels, loc="center")

    plt.show()




# s = requests.Session()
# s.auth = ('imunizacao_public', 'qlto5t&7r_@+#Tlstigi')
# response = s.post('https://imunizacao-es.saude.gov.br/_search?scroll=1m')
# list_result = response.text.split(',')
# _scroll_id = list_result[0].replace('{"_scroll_id":"', '').replace('"', '')

# ufs = []
# while True:
#     s = requests.Session()
#     s.auth = ('imunizacao_public', 'qlto5t&7r_@+#Tlstigi')
#     s.params = _scroll_id
#     response = s.post('https://imunizacao-es.saude.gov.br/_search?scroll=1m')
#     list_result = response.text.split(',')
#     _scroll_id = list_result[0].replace('{"_scroll_id":"', '').replace('"', '')
#
#     for index, li in enumerate(list_result):
#         if 'estabelecimento_uf' in li:
#             print(str(li)[33:35])
#             ufs.append(str(li)[33:35])

    # _scroll_id = list_result[0].replace('{"_scroll_id":"', '').replace('"', '')
    # print(_scroll_id)


