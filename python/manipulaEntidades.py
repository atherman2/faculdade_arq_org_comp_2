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

    procCacheRequisitante: ProcessadorCache = conjuntoProcCaches.procCaches[indiceProcCacheRequisitante]
    linhaComTagCorrespondente: LinhaCache = buscaLinhaCache(procCacheRequisitante, tag)

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
    encontrouLinhaEmOutraCache, linhasEncontradasEmOutrasCaches, indicesProcCaches = buscaLinhaEmOutrasCaches(conjuntoProcCaches, tag, indiceProcCacheRequisitante)
    
    encontrouLinhaEmOutraCache = False
    estadoNaOutraCache = EstadoMesif.NOTFOUND
    for i, linha in enumerate(linhasEncontradasEmOutrasCaches):
    
        if linha.estadoMesif in (EstadoMesif.EXCLUSIVE, EstadoMesif.MODIFIED, EstadoMesif.FORWARD):

            estadoNaOutraCache = linha.estadoMesif
            linhaEncontradaEmOutraCache = linha
    
    # Se terminou a procura em outras caches tendo encontrado a linha com estado diferente de inválido
    if encontrouLinhaEmOutraCache and (estadoNaOutraCache in (EstadoMesif.EXCLUSIVE, EstadoMesif.MODIFIED, EstadoMesif.FORWARD)):

        # Se não havia encontrado linha na cache requisitante (substituir uma linha existente ou adicionar linha)
        if linhaComTagCorrespondente == None:

            linhaSubstituicao: LinhaCache = procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao]

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

def buscaLinhaEmOutrasCaches(conjuntoProcCaches: ConjuntoProcessadoresCaches, tag: int, indiceProcCacheRequisitante: int):

    indiceProcCacheAtual = 0
    encontrouLinhaEmOutraCache = False
    indicesProcCaches = []
    linhasEncontradasEmOutrasCaches = []
    while (not encontrouLinhaEmOutraCache) and (indiceProcCacheAtual < conjuntoProcCaches.quantidadeProcCaches):

        # Verificação para não realizar a busca da linha na própria cache requisitante mais uma vez
        if indiceProcCacheAtual != indiceProcCacheRequisitante:

            # Realiza a busca na cache do índice atual
            linhaProcCacheAtual: LinhaCache = buscaLinhaCache(conjuntoProcCaches.procCaches[indiceProcCacheAtual], tag)
            
            # Se encontrou a linha na cache atual
            if linhaProcCacheAtual != None:

                encontrouLinhaEmOutraCache = True
                linhasEncontradasEmOutrasCaches.append(linhaProcCacheAtual)
                indicesProcCaches.append(indiceProcCacheAtual)

        indiceProcCacheAtual += 1
    
    return encontrouLinhaEmOutraCache, linhasEncontradasEmOutrasCaches, indicesProcCaches

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

def trataSubstituicao(linhaSubstituicao: LinhaCache, conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal, indiceProcCacheRequisitante: int):

    if linhaSubstituicao.estadoMesif == EstadoMesif.MODIFIED:

        endereco = linhaSubstituicao.tag * memoriaPrincipal.palavrasPorBloco
        escreverBlocoMemoriaPrincipal(memoriaPrincipal, endereco, linhaSubstituicao.palavras)
    
    elif linhaSubstituicao.estadoMesif == EstadoMesif.FORWARD:

        trataLinhaSubstituicaoForward(linhaSubstituicao, conjuntoProcCaches, indiceProcCacheRequisitante)

def trataLinhaSubstituicaoForward(linhaSubstituicao: LinhaCache, conjuntoProcCaches: ConjuntoProcessadoresCaches, indiceProCacheRequisitante: int):

    encontrouLinhaEmOutrasCaches, linhasEncontradasEmOutrasCaches, indicesProcCaches = buscaLinhaEmOutrasCaches(conjuntoProcCaches, linhaSubstituicao.tag, indiceProCacheRequisitante)
    primeiraLinhaShared = None
    for linha in linhasEncontradasEmOutrasCaches:

        if (primeiraLinhaShared == None) and (linha.estadoMesif == EstadoMesif.SHARED):

            linha.estadoMesif = EstadoMesif.FORWARD
            primeiraLinhaShared = linha

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