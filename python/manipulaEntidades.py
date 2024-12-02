from entidades import *

def lerPalavra(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal, endereco: int, indiceProcCacheRequisitante: int):

    palavrasPorLinha = conjuntoProcCaches.procCaches[indiceProcCacheRequisitante].palavrasPorLinha
    tag = endereco//palavrasPorLinha
    indicePalavra = endereco % palavrasPorLinha

    procCacheRequisitante = conjuntoProcCaches.procCaches[indiceProcCacheRequisitante]
    linhaComTagCorrespondente = buscaLinhaCache(procCacheRequisitante, tag)

    if linhaComTagCorrespondente != None:

        if linhaComTagCorrespondente.tag != EstadoMesif.INVALID:

            # TODO: Exibir Cache Hit
            encontrouLinhaValida = True
            return linhaComTagCorrespondente.palavras[indicePalavra]
    
    # TODO: Exibir Cache Miss
    indiceProcCacheAtual = 0
    encontrouLinhaForward = False
    while (not encontrouLinhaForward) and (indiceProcCacheAtual < conjuntoProcCaches.quantidadeProcCaches):

        if indiceProcCacheAtual != indiceProcCacheRequisitante:

            linhaAlvoProcCacheAtual: LinhaCache = buscaLinhaCache(conjuntoProcCaches.procCaches[indiceProcCacheAtual])
            if linhaAlvoProcCacheAtual.estadoMesif == EstadoMesif.FORWARD:

                encontrouLinhaForward = True
                linhaForward = linhaAlvoProcCacheAtual
    
    if encontrouLinhaForward:

        if linhaComTagCorrespondente == None:

            copiaLinha(linhaForward, procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao], procCacheRequisitante.palavrasPorLinha)
            procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao].estadoMesif = EstadoMesif.SHARED
            
            procCacheRequisitante.indiceSubstituicao += 1
            if procCacheRequisitante.indiceSubstituicao == procCacheRequisitante.quantidadeDeLinhas:
                
                procCacheRequisitante.indiceSubstituicao = 0

def buscaLinhaCache(procCache: ProcessadorCache, tag) -> LinhaCache:

    indiceLinhaCacheAtual = 0
    encontrou = False
    while (not encontrou) and (indiceLinhaCacheAtual < procCache.quantidadeDeLinhas):

        encontrou = (procCache.linhas[indiceLinhaCacheAtual].tag == tag)
        if not encontrou:
        
            indiceLinhaCacheAtual += 1
    if encontrou:
        
        return procCache.linhas[indiceLinhaCacheAtual]

def copiaLinha(linhaFonte: LinhaCache, linhaDestino: LinhaCache, tamanhoLinha: int):

    linhaDestino.tag = linhaFonte.tag
    linhaDestino.sendoUsada = linhaFonte.sendoUsada

    for indicePalvraAtual in range(tamanhoLinha):
        
        copiaPalavra(linhaFonte.palavras[indicePalvraAtual], linhaDestino.palavras[indicePalvraAtual])

def copiaPalavra(palavraFonte: Palavra, palavraDestino: Palavra):

    palavraDestino.conteudo = palavraFonte.conteudo
    palavraDestino.sendoUsada =  palavraFonte.sendoUsada