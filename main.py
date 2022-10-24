import locale
import sys
from datetime import datetime
import config
import requests
from dao.sqlite_dao_factory import SqliteDAOFactory

from models.cotacao import Cotacao

url = f'https://api.hgbrasil.com/finance?key={config.api_key}'

locale.setlocale(locale.LC_ALL, '')
data_hora_hoje = str(datetime.today().date().strftime('%A, %x'))
cotacao_DAO = None
cotacao_hoje = None


def consultar_dados_financeiros() -> Cotacao:
    requisicao = requests.get(url)
    dados = requisicao.json()['results']['currencies']

    dolar = float(dados['USD']['buy'])
    euro = float(dados['EUR']['buy'])
    data_hora = str(datetime.now())
    return Cotacao(dolar=dolar, euro=euro, data_hora=data_hora)

def salvar_cotacao(cotacao) -> None:
    cotacao_DAO.adicionar(cotacao)

def carregar_cotacao_hoje() -> Cotacao:

    registro_cotacao_hoje = cotacao_DAO.buscar_cotacao_hoje()

    if registro_cotacao_hoje is None:
        cotacao = consultar_dados_financeiros()
        salvar_cotacao(cotacao)
        return cotacao
    else:
        registro_cotacao_hoje = cotacao_DAO.buscar_cotacao_hoje()
        return Cotacao(registro_cotacao_hoje[0], registro_cotacao_hoje[1],
                       registro_cotacao_hoje[2], registro_cotacao_hoje[3])

def mostrar_menu():
    print(f'Cotação: {data_hora_hoje}')
    print(f'Dólar: {cotacao_hoje.dolar}')
    print(f'Euro: {cotacao_hoje.euro}')
    print('Digite um valor em R$ ou ZERO para SAIR:')

    valor_reais = float(input('R$'))

    if valor_reais > 0.0:
        real_em_dolar = valor_reais / cotacao_hoje.dolar
        real_em_euro = valor_reais / cotacao_hoje.euro
        print(f'\n R$ {valor_reais} = US$ {real_em_dolar}')
        print(f'\n R$ {valor_reais} = € {real_em_euro}')
        print('\n')
        mostrar_menu()
    else:
        sys.exit('Fim')

if __name__ == '__main__':
    sqliteFactory = SqliteDAOFactory()
    cotacao_DAO = sqliteFactory.cotacao_dao
    cotacao_hoje = carregar_cotacao_hoje()
    mostrar_menu()