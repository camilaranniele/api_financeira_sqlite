import sqlite3
import dao.sqlite_dao_factory as dao

from dao.cotacao_dao import CotacaoDao


class SqliteCotacaoDao(CotacaoDao):

    def adicionar(self, cotacao):
        conexao = dao.SqliteDAOFactory.criar_conexao()
        cursor = conexao.cursor()
        query = 'INSERT INTO Cotacao VALUES (null,?,?,?)'
        registro = (cotacao.dolar, cotacao.euro, cotacao.data_hora)

        try:
            cursor.execute(query, registro)
            conexao.commit()
        except sqlite3.Error as e:
            raise Exception(f'Erro: {e}')
        finally:
            if conexao:
                conexao.close()

    def selecionar_cotacao(self, limit=10) -> list:
        conexao = dao.SqliteDAOFactory.criar_conexao()
        cursor = conexao.cursor()
        query = 'SELECT * FROM Cotacao ORDER BY data_hora LIMIT ?'

        try:
            dados = cursor.execute(query, (limit, )).fetchall()
            conexao.commit()
        except sqlite3.Error as e:
            raise Exception(f'Erro: {e}')
        finally:
            if conexao:
                conexao.close()

    def excluir(self, id):
        conexao = dao.SqliteDAOFactory.criar_conexao()
        cursor = conexao.cursor()
        query = 'DELETE FROM Cotacao WHERE id_cotacao = ?'

        try:
            cursor.execute(query, (id, ))
            conexao.commit()
        except sqlite3.Error as e:
            raise Exception(f'Erro: {e}')
        finally:
            if conexao:
                conexao.close()

    def buscar_cotacao_hoje(self):
        conexao = dao.SqliteDAOFactory.criar_conexao()
        cursor = conexao.cursor()
        query = 'SELECT * FROM Cotacao WHERE DATE(data_hora) = DATE()'

        try:
            dados = cursor.execute(query).fetchone()
            conexao.commit()
        except sqlite3.Error as e:
            raise Exception(f'Erro: {e}')
        finally:
            if conexao:
                conexao.close()

        return dados