from classesSimulador import *
from controlaSimulador import *

def exibirTodos(lista):

    for string in lista:

        print(string, end="")

class OpTeste(Enum):

    ESCRITA = auto()
    LEITURA = auto()

class TestaMemoria():

    def __init__(self, cjtoCaches, memPrinc):
        
        self.cjtoCaches: ConjuntoProcessadoresCaches = cjtoCaches
        self.memPrinc: MemoriaPrincipal = memPrinc
        self.listaEscrita = []
        self.tamanhoListaEscrita = 0
        self.operacoes = {
            OpTeste.ESCRITA: self.opEscrita,
            OpTeste.LEITURA: self.opLeitura
        }

    def leitura(self, endereco, indiceCache):

        return lerPalavra(self.cjtoCaches, self.memPrinc, endereco, indiceCache)
    
    def escrita(self, endereco, indiceCache, conteudoNovaPalavra):

        return escreverPalavra(self.cjtoCaches, self.memPrinc, endereco, indiceCache, conteudoNovaPalavra)
    
    def exibeCaches(self):

        exibirTodos(self.cjtoCaches.paraArrayStrings())

    def exibeInfoLeitura(self, endereco, indiceCache):

        leit = self.leitura(endereco, indiceCache)
        valorLido = leit[0].conteudo
        log = leit[1]
        exibirTodos(log)
        self.exibeCaches()
        return valorLido

    def exibeInfoEscrita(self, endereco, indiceCache, conteudoNovaPalavra):

        log = self.escrita(endereco, indiceCache, conteudoNovaPalavra)
        exibirTodos(log)
        self.exibeCaches()
    
    def inserirListaEscrita(self, vetorInfo):

        encontrou = False
        
        for indiceEscrita in range(self.tamanhoListaEscrita):

            if self.listaEscrita[indiceEscrita][0] == vetorInfo[0]:

                self.listaEscrita[indiceEscrita][1] = vetorInfo[1]
                encontrou = True
        
        if not encontrou:

            self.listaEscrita.append(vetorInfo)
            self.tamanhoListaEscrita += 1
    
    def consultarListaEscrita(self, vetorInfo):

        valorEncontrado = None

        for indiceEscrita in range(self.tamanhoListaEscrita):

            if self.listaEscrita[indiceEscrita][0] == vetorInfo[0]:

                valorEncontrado = self.listaEscrita[indiceEscrita][1]
                
        return valorEncontrado

    def opEscrita(self, vetorInfo):

        self.exibeInfoEscrita(vetorInfo[0], vetorInfo[1], vetorInfo[2])
        self.inserirListaEscrita([vetorInfo[0], vetorInfo[2]])
    
    def opLeitura(self, vetorInfo):

        valorLido = self.exibeInfoLeitura(vetorInfo[0], vetorInfo[1])
        ultimoValorEscrito = self.consultarListaEscrita([vetorInfo[0]])
        # print(f"ultimoValorEscrito = {ultimoValorEscrito}, valorLido = {valorLido}")
        assert ultimoValorEscrito == valorLido, f"ultimoValorEscrito = {ultimoValorEscrito}, valorLido = {valorLido}"

    def execOps(self, vetorOperacoes):

        for operacao in vetorOperacoes:

            self.operacoes[operacao[0]](operacao[1])

def test_1(cjtoCaches: ConjuntoProcessadoresCaches, memPrinc: MemoriaPrincipal):

    testaMemoria = TestaMemoria(cjtoCaches, memPrinc)
    testaMemoria.execOps([[OpTeste.ESCRITA, [3, 0, 115]]])
    testaMemoria.execOps([[OpTeste.LEITURA, [3, 1]]])
    
    for i in range(2):
        testaMemoria.execOps([[OpTeste.ESCRITA, [4+i, 2, 116+i]]])
        testaMemoria.execOps([[OpTeste.LEITURA, [4+i, 3]]])
    
    testaMemoria.execOps([[OpTeste.ESCRITA, [3, 1, 120]]])
    testaMemoria.execOps([[OpTeste.LEITURA, [4, 2]]])
    testaMemoria.execOps([[OpTeste.LEITURA, [3, 0]]])

def test_2(cjtoCaches: ConjuntoProcessadoresCaches, memPrinc: MemoriaPrincipal):

    testaMemoria = TestaMemoria(cjtoCaches, memPrinc)
    testaMemoria.execOps([[OpTeste.ESCRITA,[3, 0, 115]],
                          [OpTeste.LEITURA,[3, 1]],

                          [OpTeste.ESCRITA,[4, 2, 116]],
                          [OpTeste.LEITURA,[4, 3]],
                          [OpTeste.ESCRITA,[5, 2, 117]],
                          [OpTeste.LEITURA,[5, 3]],
                          
                          [OpTeste.ESCRITA,[3, 1, 120]],
                          [OpTeste.LEITURA,[4, 2]],
                          [OpTeste.LEITURA,[3, 0]]])

def test_3(cjtoCaches: ConjuntoProcessadoresCaches, memPrinc: MemoriaPrincipal):

    testaMemoria = TestaMemoria(cjtoCaches, memPrinc)
    testaMemoria.execOps([
        # Teste 1: Escrita seguida de múltiplas leituras
        [OpTeste.ESCRITA, [0, 0, 100]],
        [OpTeste.LEITURA, [0, 1]],
        [OpTeste.LEITURA, [0, 2]],
        [OpTeste.LEITURA, [0, 3]],

        # Teste 2: Múltiplas escritas e leituras no mesmo endereço
        [OpTeste.ESCRITA, [1, 0, 150]],
        [OpTeste.LEITURA, [1, 1]],
        [OpTeste.ESCRITA, [1, 2, 151]],
        [OpTeste.LEITURA, [1, 3]],
        [OpTeste.ESCRITA, [1, 0, 152]],
        [OpTeste.LEITURA, [1, 1]],

        # Teste 3: Padrão ping-pong com escritas antes das leituras
        [OpTeste.ESCRITA, [2, 0, 200]],
        [OpTeste.ESCRITA, [3, 1, 201]],
        [OpTeste.LEITURA, [2, 2]],
        [OpTeste.LEITURA, [3, 3]],
        [OpTeste.ESCRITA, [2, 0, 202]],
        [OpTeste.LEITURA, [2, 1]],

        # Teste 4: Sequencial com garantia de escrita prévia
        [OpTeste.ESCRITA, [4, 0, 250]],
        [OpTeste.ESCRITA, [5, 0, 251]],
        [OpTeste.ESCRITA, [6, 0, 252]],
        [OpTeste.LEITURA, [4, 1]],
        [OpTeste.LEITURA, [5, 1]],
        [OpTeste.LEITURA, [6, 1]],
        [OpTeste.LEITURA, [6, 1]]
    ])

if __name__ == "__main__":

    memoriaPrincipal = MemoriaPrincipal()
    conjuntoProcCaches = ConjuntoProcessadoresCaches()

    QUANTIDADE_PALAVRAS = 2

    QUANTIDADE_CACHES = 4
    QUANTIDADE_LINHAS = 8

    QUANTIDADE_BLOCOS = 64
    
    INTERVALO_ALEATORIEDADE = Intervalo(0, 999)

    memoriaPrincipal.intervaloAleatoriedadePalavras = INTERVALO_ALEATORIEDADE

    memoriaPrincipal.palavrasPorBloco = QUANTIDADE_PALAVRAS
    memoriaPrincipal.quantidadeDeBlocos = QUANTIDADE_BLOCOS
    memoriaPrincipal.constroi()

    conjuntoProcCaches.quantidadeProcCaches = QUANTIDADE_CACHES
    conjuntoProcCaches.intervalorAleatoriedadePalavras = INTERVALO_ALEATORIEDADE
    conjuntoProcCaches.palavrasPorLinha = QUANTIDADE_PALAVRAS
    conjuntoProcCaches.linhasPorProcCache = QUANTIDADE_LINHAS
    conjuntoProcCaches.constroi()
    
    test_3(conjuntoProcCaches, memoriaPrincipal)