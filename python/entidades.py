from enum import Enum, auto
from random import randint

class EstadoMesif(Enum):

    MODIFIED = 0
    EXCLUSIVE = 1
    SHARED = 2
    INVALID = 3
    FORWARD = 4
    EMPTY = 5
    NOTFOUND = 6

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

        self.linhas: list[LinhaCache] = []
        indiceLinhaAtual = 0
        while indiceLinhaAtual < self.quantidadeDeLinhas:

            self.linhas.append(LinhaCache(self))
            indiceLinhaAtual += 1

class LinhaCache:

    def __init__(self, processadorCache: ProcessadorCache):

        self.sendoUsada = False
        self.tag = -1
        self.estadoMesif = EstadoMesif.EMPTY
        
        self.palavras: list[Palavra] = []
        indicePalavraAtual = 0
        while indicePalavraAtual < processadorCache.palavrasPorLinha:

            self.palavras.append(Palavra(processadorCache.intervaloAleatoriedadePalavras))
            indicePalavraAtual += 1

class ConjuntoProcessadoresCaches:

    def __init__(self):
        
        self.quantidadeProcCaches = 0
        self.procCaches = None
    
    def constroi(self):

        self.procCaches: list[ProcessadorCache] = []
        indiceProcCacheAtual = 0
        while indiceProcCacheAtual < self.quantidadeProcCaches:

            self.procCaches.append(ProcessadorCache())
            indiceProcCacheAtual += 1
    
    def paraArrayStrings(self):

        arrayStrings = []
        for indiceProcCache, procCache in enumerate(self.procCaches):
            arrayStrings.append(f"CACHE #{indiceProcCache + 1}\n")
            arrayStrings.append("\n")
            for indiceLinha, linha in enumerate(procCache.linhas):
                arrayStrings.append(f"        Linha #{indiceLinha + 1}\n")
                if linha.sendoUsada:
                    arrayStrings.append(f"        - Tag: {linha.tag}\n")
                    arrayStrings.append(f"        - Palavras:\n")
                    for palavra in linha.palavras:
                        arrayStrings.append(f"            {palavra.conteudo}\n")
            arrayStrings.append("\n")
        arrayStrings.append("\n")

        return arrayStrings

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