from interface import *

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
    
    gerenciaProdutos = GerenciaProdutos()
    gerenciaProdutos.maximoProdutos = 16

    interface = Interface(conjuntoProcCaches, memoriaPrincipal, gerenciaProdutos)

    interface.executaOperacoesPorComando([[Operacao.CADASTRO, "Banana", 200, 2, 1, 1],
                                          [Operacao.CADASTRO, "Maçã", 80, 3, 2, 2],
                                          [Operacao.CADASTRO, "Uva", 40, 4, 3, 0],
                                          [Operacao.CADASTRO, "Abacate", 15, 5, 3, 0],
                                          [Operacao.CADASTRO, "Limão", 70, 3, 2, 1],
                                          [Operacao.CADASTRO, "Jaca", 15, 8, 5, 1],
                                          [Operacao.CADASTRO, "Pera", 20, 4, 3, 1],
                                          [Operacao.CADASTRO, "Lichia", 7, 4, 2, 1]])
    
    interface.mainloop()
    