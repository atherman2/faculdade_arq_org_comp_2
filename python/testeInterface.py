from interface import *

if __name__ == "__main__":

    memoriaPrincipal = MemoriaPrincipal()
    conjuntoProcCaches = ConjuntoProcessadoresCaches()

    QUANTIDADE_PALAVRAS = 2

    QUANTIDADE_CACHES = 4
    QUANTIDADE_LINHAS = 2

    QUANTIDADE_BLOCOS = 32
    
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
    
    gerenciaProdutos = GerenciaProdutos()
    gerenciaProdutos.maximoProdutos = 16

    interface = Interface(conjuntoProcCaches, memoriaPrincipal, gerenciaProdutos)
    
    interface.memPrinc.blocos[3].palavras[1].conteudo = 7

    interface.gerProd.adicionaProduto("Banana") #0
    interface.gerProd.adicionaProduto("Maçã") #1
    interface.gerProd.adicionaProduto("Uva") #2
    interface.gerProd.adicionaProduto("Abacate") #3
    interface.gerProd.adicionaProduto("Limão") #4
    interface.gerProd.adicionaProduto("Jaca") #5
    interface.gerProd.adicionaProduto("Pera") #6
    interface.gerProd.adicionaProduto("Lixia") #7

    interface.consultaProdutoSilenciosa("Lixia")
    interface.consultaProdutoSilenciosa("Lixia")

    interface.framePrincipal.frameTesteMenu.mercadoAtual = 2

    interface.consultaProdutoSilenciosa("Lixia")

    interface.framePrincipal.frameTesteMenu.mercadoAtual = 0

    interface.consultaProdutoSilenciosa("Lixia")
    
    interface.mainloop()
    