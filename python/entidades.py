from enum import Enum, auto
import random

class EstadoMesif(Enum):

    MODIFIED = 0
    EXCLUSIVE = 1
    SHARED = 2
    INVALID = 3
    FORWARD = 4

class ProcessadorCache:
    
    def __init__(self):
        
        self.linhas = None
        self.quantidadeDeLinhas = 0
    
    class LinhaCache:

        def __init__(self):

            self.palavras = None
            self.quantidadeDePalavras = 0

class MemoriaPrincipal:

    def __init__(self):

        self.blocos = None
        self.quantidadeDeBlocos = 0
        self.palavrasPorBloco = 0
    
    def setQuantidadeDeBlocos(self, quantidade):

        self.quantidadeDeBlocos = quantidade

    def setPalavrasPorBloco(self, palavrasPorBloco):

        self.palavrasPorBloco = palavrasPorBloco

    def constroi(self):

        if(self.quantidadeDeBlocos != 0):
            
            self.blocos = [self.BlocoMp()] * self.quantidadeDeBlocos

    class BlocoMp:

        def __init__(self):

            self.palavras = None
            self.quantidadeDePalavras = 0