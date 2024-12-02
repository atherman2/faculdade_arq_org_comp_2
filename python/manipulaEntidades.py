from entidades import *

# PROCESSOS GERAIS - CACHE E MEMORIA PRINCIPAL /////////////////////////////////////////////////////////////////////////////////////////////

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
    encontrouLinhaEmOutraCache = False
    while (not encontrouLinhaEmOutraCache) and (indiceProcCacheAtual < conjuntoProcCaches.quantidadeProcCaches):

        if indiceProcCacheAtual != indiceProcCacheRequisitante:

            linhaProcCacheAtual: LinhaCache = buscaLinhaCache(conjuntoProcCaches.procCaches[indiceProcCacheAtual])
            estadoMesifAtual: EstadoMesif = linhaProcCacheAtual.estadoMesif
            if (estadoMesifAtual == EstadoMesif.FORWARD) or (estadoMesifAtual == EstadoMesif.MODIFIED) or (estadoMesifAtual == EstadoMesif.EXCLUSIVE):

                encontrouLinhaEmOutraCache = True
                linhaEncontradaEmOutraCache = linhaProcCacheAtual
    
    if encontrouLinhaEmOutraCache:

        if linhaComTagCorrespondente == None:

            copiaLinha(linhaEncontradaEmOutraCache, procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao], procCacheRequisitante.palavrasPorLinha)

            if linhaEncontradaEmOutraCache.estadoMesif == EstadoMesif.FORWARD:

                procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao].estadoMesif = EstadoMesif.SHARED
            else:

                procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao].estadoMesif = EstadoMesif.FORWARD

            palavraLida = procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao].palavras[indicePalavra]

            atualizaIndiceDeSubstituicao(procCacheRequisitante)

        else:

            copiaLinha(linhaEncontradaEmOutraCache, linhaComTagCorrespondente, procCacheRequisitante.palavrasPorLinha)
            
            if linhaEncontradaEmOutraCache.estadoMesif == EstadoMesif.FORWARD:

                linhaComTagCorrespondente.estadoMesif = EstadoMesif.SHARED
            else:

                linhaComTagCorrespondente.estadoMesif = EstadoMesif.FORWARD

            palavraLida = linhaComTagCorrespondente.palavras[indicePalavra]
        
        if linhaEncontradaEmOutraCache.estadoMesif == EstadoMesif.MODIFIED:

            #TODO: Escrever na MP (write-back)
            pass
        if linhaEncontradaEmOutraCache.estadoMesif != EstadoMesif.FORWARD:

            linhaEncontradaEmOutraCache.estadoMesif = EstadoMesif.SHARED
    else:
        #TODO: Ler da MP
        pass
    
    return palavraLida

# PROCESSOS CACHE //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

    copiaVetorDePalavras(linhaFonte.palavras, linhaDestino.palavras)

def atualizaIndiceDeSubstituicao(procCache: ProcessadorCache):

    procCache.indiceSubstituicao += 1
    if procCache.indiceSubstituicao == procCache.quantidadeDeLinhas:

        procCache.indiceSubstituicao = 0

# PROCESSOS MEMÓRIA PRINCIPAL //////////////////////////////////////////////////////////////////////////////////////////////////////////////

def lerBlocoMemoriaPrincipal(memoriaPrincipal: MemoriaPrincipal, endereco: int):

    #TODO: Exibir leitura na memória principal

    palavrasPorBloco = memoriaPrincipal.palavrasPorBloco
    indiceBloco = endereco//palavrasPorBloco

    return memoriaPrincipal.blocos[indiceBloco]

# PROCESSOS USADOS TANTO EM CACHE QUANTO EM MEMÓRIA PRINCIPAL //////////////////////////////////////////////////////////////////////////////

def copiaVetorDePalavras(vetorDePalavrasFonte: list[Palavra], vetorDePalavrasDestino: list[Palavra], tamanhoVetorDePalavras):

    for indicePalavraAtual in range(tamanhoVetorDePalavras):

        copiaPalavra(vetorDePalavrasFonte[indicePalavraAtual], vetorDePalavrasDestino[indicePalavraAtual])

def copiaPalavra(palavraFonte: Palavra, palavraDestino: Palavra):

    palavraDestino.conteudo = palavraFonte.conteudo
    palavraDestino.sendoUsada =  palavraFonte.sendoUsada