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
        self.indiceSubstituicao = 0
    
    def constroi(self):

        self.linhas = []
        indiceLinhaAtual = 0
        while indiceLinhaAtual < self.quantidadeDeLinhas:

            self.linhas.append(LinhaCache(self))
            indiceLinhaAtual += 1

class LinhaCache:

    def __init__(self, processadorCache: ProcessadorCache):

        self.sendoUsada = False
        self.tag = -1
        self.estadoMesif = EstadoMesif.EMPTY
        
        self.palavras = []
        indicePalavraAtual = 0
        while indicePalavraAtual < processadorCache.palavrasPorLinha:

            self.palavras.append(Palavra(processadorCache.intervaloAleatoriedadePalavras))
            indicePalavraAtual += 1

class ConjuntoProcessadoresCaches:

    def __init__(self):
        
        self.quantidadeProcCaches = 0
        self.procCaches = None
    
    def constroi(self):

        self.procCaches = []
        indiceProcCacheAtual = 0
        while indiceProcCacheAtual < self.quantidadeProcCaches:

            self.procCaches.append(ProcessadorCache())
            indiceProcCacheAtual += 1

class MemoriaPrincipal:

    def __init__(self):

        self.blocos = None
        self.intervaloAleatoriedadePalavras = None
        self.quantidadeDeBlocos = 0
        self.palavrasPorBloco = 0

    def constroi(self):
        
        self.blocos = []
        indiceBlocoAtual = 0
        while indiceBlocoAtual < self.quantidadeDeBlocos:

           self.blocos.append(BlocoMp(self))
           indiceBlocoAtual += 1

class BlocoMp:

    def __init__(self, memoriaPrincipal: MemoriaPrincipal):

        self.sendoUsada = False
        self.palavras = []
        indicePalavraAtual = 0
        while indicePalavraAtual < memoriaPrincipal.palavrasPorBloco:

            self.palavras.append(Palavra(memoriaPrincipal.intervaloAleatoriedadePalavras))
            indicePalavraAtual += 1