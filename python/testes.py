from python.classesSimulador import *
from python.controlaSimulador import *

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

if __name__ == "__main__":

    memoriaPrincipal = MemoriaPrincipal()
    conjuntoProcCaches = ConjuntoProcessadoresCaches()

    QUANTIDADE_PALAVRAS = 2

    QUANTIDADE_CACHES = 4
    QUANTIDADE_LINHAS = 2

    QUANTIDADE_BLOCOS = 4
    
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
    
    test_leitura(conjuntoProcCaches, memoriaPrincipal)