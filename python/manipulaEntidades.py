from entidades import *

# PROCESSOS GERAIS - CACHE E MEMORIA PRINCIPAL /////////////////////////////////////////////////////////////////////////////////////////////

def lerPalavra(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal, endereco: int, indiceProcCacheRequisitante: int):

    # Cálculo de tag e índice da palavra a ser lida dentro da linha da cache

    palavrasPorLinha = conjuntoProcCaches.procCaches[indiceProcCacheRequisitante].palavrasPorLinha
    tag = endereco//palavrasPorLinha
    indicePalavra = endereco % palavrasPorLinha

    print(f'''LEITURA: iniciando leitura
    do endereco {endereco}
    de tag {tag}
    requisitada pela cache {indiceProcCacheRequisitante + 1}\n''')

    procCacheRequisitante = conjuntoProcCaches.procCaches[indiceProcCacheRequisitante]
    linhaComTagCorrespondente = buscaLinhaCache(procCacheRequisitante, tag)

    # Se encontrou a linha na cache requisitante
    if linhaComTagCorrespondente != None:

        # Se a linha encontrada na cache requisitante tem estado MESIF diferente de inválido
        if linhaComTagCorrespondente.tag != EstadoMesif.INVALID:

            # Cache hit: retornar a palavra da linha da cache requisitante
            # de acordo com o seu índice
            # TODO: Exibir Cache Hit
            print(f'''    CACHE: Hit de Leitura''')
            palavraLida = linhaComTagCorrespondente.palavras[indicePalavra]
            print(f'''        palavra lida: {palavraLida.conteudo}\n''')
            return palavraLida
    
    # Se não saiu da função pelo return, então significa que não houve Cache Hit, logo deve-se
    # procurar em outras caches
    # TODO: Exibir Cache Miss
    print(f'''    CACHE: Miss de Leitura''')
    indiceProcCacheAtual = 0
    encontrouLinhaEmOutraCache = False
    while (not encontrouLinhaEmOutraCache) and (indiceProcCacheAtual < conjuntoProcCaches.quantidadeProcCaches):

        # Verificação para não realizar a busca da linha na própria cache requisitante mais uma vez
        if indiceProcCacheAtual != indiceProcCacheRequisitante:

            # Realiza a busca na cache do índice atual
            linhaProcCacheAtual: LinhaCache = buscaLinhaCache(conjuntoProcCaches.procCaches[indiceProcCacheAtual], tag)
            
            # Se encontrou a linha na cache atual
            if linhaProcCacheAtual != None:

                estadoMesifAtual: EstadoMesif = linhaProcCacheAtual.estadoMesif
                
                # Se o estado mesif da linha encontrada em outra cache for diferente de invalid e
                # diferente de shared, parar a busca e guardar a linha encontrada
                if (estadoMesifAtual == EstadoMesif.FORWARD) or (estadoMesifAtual == EstadoMesif.MODIFIED) or (estadoMesifAtual == EstadoMesif.EXCLUSIVE):

                    encontrouLinhaEmOutraCache = True
                    linhaEncontradaEmOutraCache = linhaProcCacheAtual
        
        indiceProcCacheAtual += 1
    
    # Se terminou a procura em outras caches tendo encontrado a linha com estado diferente de inválido
    if encontrouLinhaEmOutraCache:

        # Se não havia encontrado linha na cache requisitante (substituir uma linha existente ou adicionar linha)
        if linhaComTagCorrespondente == None:

            linhaSubstituicao = procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao]

            #TODO: tratar linha a ser substituída ter estado Forward ou Modificado

            transfereLinhaLeitura(linhaEncontradaEmOutraCache, linhaSubstituicao, procCacheRequisitante.palavrasPorLinha, memoriaPrincipal, endereco)

            palavraLida = linhaSubstituicao.palavras[indicePalavra]

            atualizaIndiceDeSubstituicao(procCacheRequisitante)

        # Se havia encontrado uma linha na cache requisitante, porém esta linha estava em estado inválido
        else:

            transfereLinhaLeitura(linhaEncontradaEmOutraCache, linhaComTagCorrespondente, procCacheRequisitante.palavrasPorLinha, memoriaPrincipal, endereco)

            palavraLida = linhaComTagCorrespondente.palavras[indicePalavra]
        
    else:
        # Se não encontrou na cache requisitante nem em outras caches
        # Leitura à memória
        
        # Se não havia encontrado linha na cache requisitante (substituir uma linha existente ou adicionar linha)
        if linhaComTagCorrespondente == None:

            linhaSubstituicao = procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao]
            
            #TODO: tratar linha a ser substituída ter estado Forward ou Modificado

            transefereBlocoParaLinha(memoriaPrincipal, endereco, linhaSubstituicao, procCacheRequisitante.palavrasPorLinha)
            
            palavraLida = linhaSubstituicao.palavras[indicePalavra]

            atualizaIndiceDeSubstituicao(procCacheRequisitante)
        
        # Se havia encontrado uma linha na cache requisitante, porém esta linha estava em estado inválido
        else:

            transefereBlocoParaLinha(memoriaPrincipal, endereco, linhaComTagCorrespondente, procCacheRequisitante.palavrasPorLinha)
            
            palavraLida = linhaComTagCorrespondente.palavras[indicePalavra]
    
    print(f'''        palavra lida: {palavraLida.conteudo}\n''')

    return palavraLida

def transefereBlocoParaLinha(memoriaPrincipal, endereco, linha: LinhaCache, tamanhoLinha):
    
    bloco = lerBlocoMemoriaPrincipal(memoriaPrincipal, endereco)
    copiaVetorDePalavras(bloco.palavras, linha.palavras, tamanhoLinha)
    linha.estadoMesif = EstadoMesif.EXCLUSIVE
    tag = endereco // memoriaPrincipal.palavrasPorBloco
    linha.tag = tag

# PROCESSOS CACHE //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def buscaLinhaCache(procCache: ProcessadorCache, tag):

    indiceLinhaCacheAtual = 0
    encontrou = False
    while (not encontrou) and (indiceLinhaCacheAtual < procCache.quantidadeDeLinhas):

        encontrou = (procCache.linhas[indiceLinhaCacheAtual].tag == tag)
        if not encontrou:
        
            indiceLinhaCacheAtual += 1
    if encontrou:
        
        return procCache.linhas[indiceLinhaCacheAtual]
    else:
        return None

def copiaLinha(linhaFonte: LinhaCache, linhaDestino: LinhaCache, tamanhoLinha: int):

    linhaDestino.tag = linhaFonte.tag
    linhaDestino.sendoUsada = linhaFonte.sendoUsada

    copiaVetorDePalavras(linhaFonte.palavras, linhaDestino.palavras, tamanhoLinha)

def atualizaIndiceDeSubstituicao(procCache: ProcessadorCache):

    procCache.indiceSubstituicao += 1
    if procCache.indiceSubstituicao == procCache.quantidadeDeLinhas:

        procCache.indiceSubstituicao = 0

def transfereLinhaLeitura(linhaEncontradaEmOutraCache: LinhaCache, linhaCacheRequisitante: LinhaCache, tamanhoLinha, memoriaPrincipal, endereco):
    
    copiaLinha(linhaEncontradaEmOutraCache, linhaCacheRequisitante, tamanhoLinha)

    if linhaEncontradaEmOutraCache.estadoMesif == EstadoMesif.FORWARD:

        linhaCacheRequisitante.estadoMesif = EstadoMesif.SHARED
    else:

        if linhaEncontradaEmOutraCache.estadoMesif == EstadoMesif.MODIFIED:

            escreverBlocoMemoriaPrincipal(memoriaPrincipal, endereco, linhaEncontradaEmOutraCache.palavras)
        else:

            linhaCacheRequisitante.estadoMesif = EstadoMesif.FORWARD
    
    linhaEncontradaEmOutraCache.estadoMesif = EstadoMesif.SHARED

def trataSubstituicao(linhaSubstituicao: LinhaCache, conjuntoProcCache: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal):

    #TODO: terminar

    if linhaSubstituicao.estadoMesif == EstadoMesif.MODIFIED:

        endereco = linhaSubstituicao.tag * memoriaPrincipal.palavrasPorBloco
        escreverBlocoMemoriaPrincipal(memoriaPrincipal, endereco, linhaSubstituicao.palavras)

# PROCESSOS MEMÓRIA PRINCIPAL //////////////////////////////////////////////////////////////////////////////////////////////////////////////

def lerBlocoMemoriaPrincipal(memoriaPrincipal: MemoriaPrincipal, endereco: int):

    #TODO: Exibir leitura na memória principal

    print(f'''    MEMÓRIA PRINCIPAL: Leitura\n''')

    palavrasPorBloco = memoriaPrincipal.palavrasPorBloco
    indiceBloco = endereco//palavrasPorBloco

    return memoriaPrincipal.blocos[indiceBloco]

def escreverBlocoMemoriaPrincipal(memoriaPrincipal: MemoriaPrincipal, endereco: int, palavras):

    #TODO: Exibir escrita na memória principal

    print(f'''    MEMÓRIA PRINCIPAL: Escrita\n''')

    palavrasPorBloco = memoriaPrincipal.palavrasPorBloco
    indiceBloco = endereco//palavrasPorBloco
    bloco = memoriaPrincipal.blocos[indiceBloco]

    copiaVetorDePalavras(palavras, bloco.palavras, memoriaPrincipal.palavrasPorBloco)

# PROCESSOS USADOS TANTO EM CACHE QUANTO EM MEMÓRIA PRINCIPAL //////////////////////////////////////////////////////////////////////////////

def copiaVetorDePalavras(vetorDePalavrasFonte: list[Palavra], vetorDePalavrasDestino: list[Palavra], tamanhoVetorDePalavras):

    for indicePalavraAtual in range(tamanhoVetorDePalavras):

        copiaPalavra(vetorDePalavrasFonte[indicePalavraAtual], vetorDePalavrasDestino[indicePalavraAtual])

def copiaPalavra(palavraFonte: Palavra, palavraDestino: Palavra):

    palavraDestino.conteudo = palavraFonte.conteudo
    palavraDestino.sendoUsada =  palavraFonte.sendoUsada