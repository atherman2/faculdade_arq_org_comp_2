from entidades import *
from manipulaEntidades import *

def test_leitura(conjuntoProcCache: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal):

    memoriaPrincipal.blocos[0].palavras[0] = 0
    memoriaPrincipal.blocos[0].palavras[1] = 1
    memoriaPrincipal.blocos[1].palavras[0] = 2
    memoriaPrincipal.blocos[1].palavras[1] = 3
    memoriaPrincipal.blocos[2].palavras[0] = 4
    memoriaPrincipal.blocos[2].palavras[1] = 5
    memoriaPrincipal.blocos[3].palavras[0] = 6
    memoriaPrincipal.blocos[3].palavras[1] = 7

if __name__ == "__main__":

    memoriaPrincipal = MemoriaPrincipal()
    conjuntoProcCache = ConjuntoProcessadoresCaches()

    QUANTIDADE_PALAVRAS = 2

    QUANTIDADE_CACHES = 4
    QUANTIDADE_LINHAS = 2

    QUANTIDADE_BLOCOS = 4
    
    INTERVALO_ALEATORIEDADE = Intervalo()
    INTERVALO_ALEATORIEDADE.inicio = 0
    INTERVALO_ALEATORIEDADE.fim = 999

    memoriaPrincipal.intervaloAleatoriedadePalavras = INTERVALO_ALEATORIEDADE

    memoriaPrincipal.palavrasPorBloco = QUANTIDADE_PALAVRAS
    memoriaPrincipal.quantidadeDeBlocos = QUANTIDADE_BLOCOS
    memoriaPrincipal.constroi()

    conjuntoProcCache.quantidadeProcCaches = QUANTIDADE_CACHES
    conjuntoProcCache.constroi()

    indiceProcCacheAtual = 0
    while indiceProcCacheAtual < QUANTIDADE_CACHES:

        procCacheAtual = conjuntoProcCache.procCaches[indiceProcCacheAtual]
        procCacheAtual.intervaloAleatoriedadePalavras = INTERVALO_ALEATORIEDADE
        procCacheAtual.palavrasPorLinha = QUANTIDADE_PALAVRAS
        procCacheAtual.quantidadeDeLinhas = QUANTIDADE_LINHAS
        procCacheAtual.constroi()