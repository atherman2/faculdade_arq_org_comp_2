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

            if indiceEscrita[indiceEscrita][0] == vetorInfo[0]:

                self.listaEscrita[indiceEscrita][1] = vetorInfo[1]
                encontrou = True
        
        if not encontrou:

            self.listaEscrita.append(vetorInfo)
            self.tamanhoListaEscrita += 1
    
    def removerListaEscrita(self, vetorInfo):

        valorEncontrado = None

        for indiceEscrita in range(self.tamanhoListaEscrita):

            if self.listaEscrita[indiceEscrita][0] == vetorInfo[0]:

                valorEncontrado = self.listaEscrita[indiceEscrita][1]
                indiceValorEncontrado = indiceEscrita
        
        if valorEncontrado != None:
        
            self.listaEscrita.pop(indiceValorEncontrado)
            self.tamanhoListaEscrita -= 1
        
        return valorEncontrado

    def opEscrita(self, vetorInfo):

        self.exibeInfoEscrita(vetorInfo[0], vetorInfo[1], vetorInfo[2])
        self.inserirListaEscrita([vetorInfo[0], vetorInfo[2]])
    
    def opLeitura(self, vetorInfo):

        valorLido = self.exibeInfoLeitura(vetorInfo[0], vetorInfo[1])
        ultimoValorEscrito = self.removerListaEscrita([vetorInfo[0]])
        print(f"ultimoValorEscrito = {ultimoValorEscrito}, valorLido = {valorLido}")

    def execOps(self, vetorOperacoes):

        for operacao in vetorOperacoes:

            self.operacoes[operacao[0]](operacao[1])

def test_leitura(conjuntoProcCache: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal):

    memoriaPrincipal.blocos[0].palavras[0].conteudo = 0

    # print(f"endereço 0 memória: {memoriaPrincipal.blocos[0].palavras[0].conteudo}")

    memoriaPrincipal.blocos[0].palavras[1].conteudo = 1

    # print(f"endereço 0 memória: {memoriaPrincipal.blocos[0].palavras[0].conteudo}")

    memoriaPrincipal.blocos[1].palavras[0].conteudo = 2

    # print(f"endereço 0 memória: {memoriaPrincipal.blocos[0].palavras[0].conteudo}")

    memoriaPrincipal.blocos[1].palavras[1].conteudo = 3
    memoriaPrincipal.blocos[2].palavras[0].conteudo = 4
    memoriaPrincipal.blocos[2].palavras[1].conteudo = 5
    memoriaPrincipal.blocos[3].palavras[0].conteudo = 6
    memoriaPrincipal.blocos[3].palavras[1].conteudo = 7

    # print(f"endereço 0 memória: {memoriaPrincipal.blocos[0].palavras[0].conteudo}")

    enderecoAtual = 0
    while enderecoAtual < 8:
        # print(f"Endereço {enderecoAtual}")
        valorAtual = lerPalavra(conjuntoProcCaches, memoriaPrincipal, enderecoAtual, 0)
        
        # print(f"endereço {enderecoAtual} valor {valorAtual.conteudo} cache {1}")
        assert enderecoAtual == valorAtual.conteudo, f"endereco {enderecoAtual} valor {valorAtual.conteudo} memória {memoriaPrincipal.blocos[enderecoAtual//memoriaPrincipal.palavrasPorBloco].palavras[enderecoAtual % memoriaPrincipal.palavrasPorBloco].conteudo}"
        valorAtual = lerPalavra(conjuntoProcCaches, memoriaPrincipal, enderecoAtual, 0)
        # print(f"endereço {enderecoAtual} valor {valorAtual.conteudo} cache {1}")
        assert enderecoAtual == valorAtual.conteudo
        valorAtual = lerPalavra(conjuntoProcCaches, memoriaPrincipal, enderecoAtual, 1)
        # print(f"endereço {enderecoAtual} valor {valorAtual.conteudo} cache {2}")
        assert enderecoAtual == valorAtual.conteudo
        valorAtual = lerPalavra(conjuntoProcCaches, memoriaPrincipal, enderecoAtual, 0)
        # print(f"endereço {enderecoAtual} valor {valorAtual.conteudo} cache {1}")
        assert enderecoAtual == valorAtual.conteudo

        enderecoAtual += 1

def test_escrita_leitura(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal):

    # logEscrita = escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0, 1)
    # logEscrita = escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 1, 2)
    # conteudoPalavraLida = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0)[0].conteudo

    logEscrita1 = escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0, 1)

    for linhaLog in logEscrita1:

        print(linhaLog, end="")

    logEscrita2 = escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 1, 2)

    for linhaLog in logEscrita2:

        print(linhaLog, end="")

    valorLido, logLeitura1 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 2)

    for linhaLog in logLeitura1:

        print(linhaLog, end="")

    estadoProcCaches = conjuntoProcCaches.paraArrayStrings()
    
    for linhaEstadoProcCaches in estadoProcCaches:

        print(linhaEstadoProcCaches, end="")

    print(f"valorLido = {valorLido.conteudo}")

def test_escrita_leitura_2(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal):

    ultimoValorEscritoEnd0 = 1
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0, ultimoValorEscritoEnd0)
    valorLidoEnd0 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0)[0].conteudo
    assert valorLidoEnd0 == ultimoValorEscritoEnd0, f"ultimoValorEscritoEnd0 = {ultimoValorEscritoEnd0}, valorLidoEnd0 = {valorLidoEnd0}"

    ultimoValorEscritoEnd0 = 1
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0, ultimoValorEscritoEnd0)
    valorLidoEnd0 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0)[0].conteudo
    assert valorLidoEnd0 == ultimoValorEscritoEnd0, f"ultimoValorEscritoEnd0 = {ultimoValorEscritoEnd0}, valorLidoEnd0 = {valorLidoEnd0}"

    ultimoValorEscritoEnd1 = 2
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 1, 1, ultimoValorEscritoEnd1)
    valorLidoEnd1 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 1, 1)[0].conteudo
    assert valorLidoEnd1 == ultimoValorEscritoEnd1, f"ultimoValorEscritoEnd1 = {ultimoValorEscritoEnd1}, valorLidoEnd1 = {valorLidoEnd1}"

    ultimoValorEscritoEnd2 = 3
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 2, 2, ultimoValorEscritoEnd2)
    valorLidoEnd2 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 2, 2)[0].conteudo
    assert valorLidoEnd2 == ultimoValorEscritoEnd2, f"ultimoValorEscritoEnd2 = {ultimoValorEscritoEnd2}, valorLidoEnd2 = {valorLidoEnd2}"

    ultimoValorEscritoEnd3 = 4
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 3, ultimoValorEscritoEnd3)
    valorLidoEnd3 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 3)[0].conteudo
    assert valorLidoEnd3 == ultimoValorEscritoEnd3, f"ultimoValorEscritoEnd3 = {ultimoValorEscritoEnd3}, valorLidoEnd3 = {valorLidoEnd3}"

    ultimoValorEscritoEnd4 = 5
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 4, 0, ultimoValorEscritoEnd4)
    valorLidoEnd4 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 4, 0)[0].conteudo
    assert valorLidoEnd4 == ultimoValorEscritoEnd4, f"ultimoValorEscritoEnd4 = {ultimoValorEscritoEnd4}, valorLidoEnd4 = {valorLidoEnd4}"

    ultimoValorEscritoEnd5 = 6
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 5, 1, ultimoValorEscritoEnd5)
    valorLidoEnd5 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 5, 1)[0].conteudo
    assert valorLidoEnd5 == ultimoValorEscritoEnd5, f"ultimoValorEscritoEnd5 = {ultimoValorEscritoEnd5}, valorLidoEnd5 = {valorLidoEnd5}"

    ultimoValorEscritoEnd6 = 7
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 6, 2, ultimoValorEscritoEnd6)
    valorLidoEnd6 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 6, 2)[0].conteudo
    assert valorLidoEnd6 == ultimoValorEscritoEnd6, f"ultimoValorEscritoEnd6 = {ultimoValorEscritoEnd6}, valorLidoEnd6 = {valorLidoEnd6}"

    ultimoValorEscritoEnd7 = 8
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 7, 3, ultimoValorEscritoEnd7)
    valorLidoEnd7 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 7, 3)[0].conteudo
    assert valorLidoEnd7 == ultimoValorEscritoEnd7, f"ultimoValorEscritoEnd7 = {ultimoValorEscritoEnd7}, valorLidoEnd7 = {valorLidoEnd7}"

    ultimoValorEscritoEnd8 = 9
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 8, 0, ultimoValorEscritoEnd8)
    valorLidoEnd8 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 8, 0)[0].conteudo
    assert valorLidoEnd8 == ultimoValorEscritoEnd8, f"ultimoValorEscritoEnd8 = {ultimoValorEscritoEnd8}, valorLidoEnd8 = {valorLidoEnd8}"

    ultimoValorEscritoEnd9 = 10
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 9, 1, ultimoValorEscritoEnd9)
    valorLidoEnd9 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 9, 1)[0].conteudo
    assert valorLidoEnd9 == ultimoValorEscritoEnd9, f"ultimoValorEscritoEnd9 = {ultimoValorEscritoEnd9}, valorLidoEnd9 = {valorLidoEnd9}"

def test_escrita_leitura_3(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal):

    ultimoValorEscritoEnd0 = 1
    log = escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0, ultimoValorEscritoEnd0)
    exibirTodos(log)
    log = conjuntoProcCaches.paraArrayStrings()
    exibirTodos(log)

    leitEnd0 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0)
    valorLidoEnd0 = leitEnd0[0].conteudo
    log = leitEnd0[1]
    exibirTodos(log)
    log = conjuntoProcCaches.paraArrayStrings()
    exibirTodos(log)
    print(f"ultimoValorEscrito = {ultimoValorEscritoEnd0}, valorLido = {valorLidoEnd0}")
    
    ultimoValorEscritoEnd0 = 1
    log = escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0, ultimoValorEscritoEnd0)
    exibirTodos(log)
    log = conjuntoProcCaches.paraArrayStrings()
    exibirTodos(log)

    leitEnd0 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 0)
    valorLidoEnd0 = leitEnd0[0].conteudo
    log = leitEnd0[1]
    exibirTodos(log)
    log = conjuntoProcCaches.paraArrayStrings()
    exibirTodos(log)
    print(f"ultimoValorEscrito = {ultimoValorEscritoEnd0}, valorLido = {valorLidoEnd0}")
    
def test_escrita_leitura_4(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal):

    # Teste 19: Mistura de padrões - simples e intensivo
    ultimoValorEscritoEnd14 = 900
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 14, 0, ultimoValorEscritoEnd14)
    lerPalavra(conjuntoProcCaches, memoriaPrincipal, 14, 1)
    for i in range(3):
        lerPalavra(conjuntoProcCaches, memoriaPrincipal, 15-i, 2)
    valorLidoEnd14 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 14, 3)[0].conteudo
    assert valorLidoEnd14 == ultimoValorEscritoEnd14, f"ultimoValorEscritoEnd14 = {ultimoValorEscritoEnd14}, valorLidoEnd14 = {valorLidoEnd14}"

    # Teste 20: Padrão intensivo seguido de simples
    ultimoValorEscritoEnd0 = 950
    for i in range(4):
        escreverPalavra(conjuntoProcCaches, memoriaPrincipal, i, i, 945 + i)
        lerPalavra(conjuntoProcCaches, memoriaPrincipal, i+1, (i+1)%4)
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 2, ultimoValorEscritoEnd0)
    valorLidoEnd0 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 0, 3)[0].conteudo
    assert valorLidoEnd0 == ultimoValorEscritoEnd0, f"ultimoValorEscritoEnd0 = {ultimoValorEscritoEnd0}, valorLidoEnd0 = {valorLidoEnd0}"

    # Teste 21: Alternância entre estilos
    ultimoValorEscritoEnd3 = 120
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 0, 115)
    lerPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 1)
    for i in range(2):
        escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 4+i, 2, 116+i)
        lerPalavra(conjuntoProcCaches, memoriaPrincipal, 5-i, 3)
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 1, ultimoValorEscritoEnd3)
    lerPalavra(conjuntoProcCaches, memoriaPrincipal, 6, 2)
    valorLidoEnd3 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 0)[0].conteudo
    assert valorLidoEnd3 == ultimoValorEscritoEnd3, f"ultimoValorEscritoEnd3 = {ultimoValorEscritoEnd3}, valorLidoEnd3 = {valorLidoEnd3}"

    # Teste 22: Combinação de padrões circulares e sequenciais
    ultimoValorEscritoEnd7 = 180
    for i in range(4):
        escreverPalavra(conjuntoProcCaches, memoriaPrincipal, i*2, i, 175+i)
    lerPalavra(conjuntoProcCaches, memoriaPrincipal, 7, 0)
    lerPalavra(conjuntoProcCaches, memoriaPrincipal, 6, 1)
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 7, 2, ultimoValorEscritoEnd7)
    valorLidoEnd7 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 7, 3)[0].conteudo
    assert valorLidoEnd7 == ultimoValorEscritoEnd7, f"ultimoValorEscritoEnd7 = {ultimoValorEscritoEnd7}, valorLidoEnd7 = {valorLidoEnd7}"

    # Teste 23: Mistura de acesso sequencial e aleatório
    ultimoValorEscritoEnd5 = 225
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 5, 0, 220)
    for i in [8, 2, 15, 4]:
        lerPalavra(conjuntoProcCaches, memoriaPrincipal, i, 1)
        escreverPalavra(conjuntoProcCaches, memoriaPrincipal, i-1, 2, 221+i)
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 5, 3, ultimoValorEscritoEnd5)
    valorLidoEnd5 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 5, 0)[0].conteudo
    assert valorLidoEnd5 == ultimoValorEscritoEnd5, f"ultimoValorEscritoEnd5 = {ultimoValorEscritoEnd5}, valorLidoEnd5 = {valorLidoEnd5}"

def test_escrita_leitura_5(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal):

    # Teste 21: Alternância entre estilos
    ultimoValorEscritoEnd3 = 120
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 0, 115)
    lerPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 1)
    
    for i in range(2):
        escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 4+i, 2, 116+i)
        lerPalavra(conjuntoProcCaches, memoriaPrincipal, 5-i, 3)
    
    escreverPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 1, ultimoValorEscritoEnd3)
    lerPalavra(conjuntoProcCaches, memoriaPrincipal, 6, 2)
    valorLidoEnd3 = lerPalavra(conjuntoProcCaches, memoriaPrincipal, 3, 0)[0].conteudo
    assert valorLidoEnd3 == ultimoValorEscritoEnd3, f"ultimoValorEscritoEnd3 = {ultimoValorEscritoEnd3}, valorLidoEnd3 = {valorLidoEnd3}"

def test_escrita_leitura_6(cjtoCaches: ConjuntoProcessadoresCaches, memPrinc: MemoriaPrincipal):

    testaMemoria = TestaMemoria(cjtoCaches, memPrinc)
    testaMemoria.execOps([[OpTeste.ESCRITA, [3, 0, 115]]])
    testaMemoria.execOps([[OpTeste.LEITURA, [3, 1]]])
    
    for i in range(2):
        testaMemoria.execOps([[OpTeste.ESCRITA, [4+i, 2, 116+i]]])
        testaMemoria.execOps([[OpTeste.LEITURA, [4+i, 3]]])
    
    testaMemoria.execOps([[OpTeste.ESCRITA, [3, 1, 120]]])
    testaMemoria.execOps([[OpTeste.LEITURA, [4, 2]]])
    testaMemoria.execOps([[OpTeste.LEITURA, [3, 0]]])

def test_escrita_leitura_7(cjtoCaches: ConjuntoProcessadoresCaches, memPrinc: MemoriaPrincipal):

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

if __name__ == "__main__":

    memoriaPrincipal = MemoriaPrincipal()
    conjuntoProcCaches = ConjuntoProcessadoresCaches()

    QUANTIDADE_PALAVRAS = 2

    QUANTIDADE_CACHES = 4
    QUANTIDADE_LINHAS = 2

    QUANTIDADE_BLOCOS = 8
    
    INTERVALO_ALEATORIEDADE = Intervalo(0, 999)

    memoriaPrincipal.intervaloAleatoriedadePalavras = INTERVALO_ALEATORIEDADE

    memoriaPrincipal.palavrasPorBloco = QUANTIDADE_PALAVRAS
    memoriaPrincipal.quantidadeDeBlocos = QUANTIDADE_BLOCOS
    memoriaPrincipal.constroi()

    conjuntoProcCaches.quantidadeProcCaches = QUANTIDADE_CACHES
    conjuntoProcCaches.constroi()

    indiceProcCacheAtual = 0
    while indiceProcCacheAtual < QUANTIDADE_CACHES:

        procCacheAtual = conjuntoProcCaches.procCaches[indiceProcCacheAtual]
        procCacheAtual.intervaloAleatoriedadePalavras = INTERVALO_ALEATORIEDADE
        procCacheAtual.palavrasPorLinha = QUANTIDADE_PALAVRAS
        procCacheAtual.quantidadeDeLinhas = QUANTIDADE_LINHAS
        procCacheAtual.constroi()

        indiceProcCacheAtual += 1
    
    test_escrita_leitura_7(conjuntoProcCaches, memoriaPrincipal)