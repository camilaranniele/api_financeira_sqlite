from abc import ABC, abstractmethod

class CotacaoDao(ABC):

    @abstractmethod
    def adicionar(self, cotacao):
        pass

    @abstractmethod
    def selecionar_cotacao(self, limit=10) -> list:
        pass

    @abstractmethod
    def excluir(self, id):
        pass

    @abstractmethod
    def buscar_cotacao_hoje(self):
        pass