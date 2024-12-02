from enum import Enum, auto
from random import randint

class EstadoMesif(Enum):

    MODIFIED = 0
    EXCLUSIVE = 1
    SHARED = 2
    INVALID = 3
    FORWARD = 4
    EMPTY = 5

class Intervalo:

    def __init__(self, inicio, fim):
        
        self.inicio = inicio
        self.fim = fim

class Palavra:

    def __init__(self, intervaloAleatoriedade: Intervalo):

        self.sendoUsada = False
        self.conteudo = randint(intervaloAleatoriedade.inicio, intervaloAleatoriedade.fim)

class ProcessadorCache:
    
    def __init__(self):
        
        self.linhas = None
        self.intervaloAleatoriedadePalavras = None
        self.quantidadeDeLinhas = 0
        self.palavrasPorLinha = 0
    
    def constroi(self):

        self.linhas = [LinhaCache(self)] * self.quantidadeDeLinhas

class LinhaCache:

        def __init__(self, processadorCache: ProcessadorCache):

            self.sendoUsada = False
            self.tag = -1
            self.estadoMesif = EstadoMesif.EMPTY
            self.palavras = Palavra(processadorCache.intervaloAleatoriedadePalavras) * processadorCache.palavrasPorLinha

class MemoriaPrincipal:

    def __init__(self):

        self.blocos = None
        self.quantidadeDeBlocos = 0
        self.palavrasPorBloco = 0

    def constroi(self):
            
        self.blocos = [BlocoMp()] * self.quantidadeDeBlocos

class BlocoMp:

    def __init__(self):

        self.palavras = None
        self.quantidadeDePalavras = 0