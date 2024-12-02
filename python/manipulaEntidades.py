from entidades import *

def lerPalavra(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal, endereco: int, indiceProcCache: int):

    palavrasPorLinha = conjuntoProcCaches.procCaches[indiceProcCache].palavrasPorLinha
    tag = endereco//palavrasPorLinha
    indicePalavra = endereco % palavrasPorLinha

    procCacheAlvo = conjuntoProcCaches.procCaches[indiceProcCache]
    linhaAlvo = buscaLinhaCache(procCacheAlvo, tag)
    encontrouLinhaValida = False
    if linhaAlvo != None:

        if linhaAlvo.tag != EstadoMesif.INVALID:

            # TODO: Exibir Cache Hit
            encontrouLinhaValida = True
            return linhaAlvo.palavras[indicePalavra]
    
    if not encontrouLinhaValida:

        # TODO: Exibir Cache Miss
        indiceProcCacheAtual = 0
        encontrouLinhaForward = False
        while (not encontrouLinhaForward) and (indiceProcCacheAtual < conjuntoProcCaches.quantidadeProcCaches):
            if indiceProcCacheAtual != indiceProcCache:
                linhaAlvoProcCacheAtual: LinhaCache = buscaLinhaCache(conjuntoProcCaches.procCaches[indiceProcCacheAtual])
                if linhaAlvoProcCacheAtual.estadoMesif == EstadoMesif.FORWARD:
                    encontrouLinhaForward = True

def buscaLinhaCache(procCache: ProcessadorCache, tag) -> LinhaCache:

    indiceLinhaCacheAtual = 0
    encontrou = False
    while (not encontrou) and (indiceLinhaCacheAtual < procCache.quantidadeDeLinhas):
        encontrou = (procCache.linhas[indiceLinhaCacheAtual].tag == tag)
        if not encontrou:
            indiceLinhaCacheAtual += 1
    if encontrou:
        return procCache.linhas[indiceLinhaCacheAtual]