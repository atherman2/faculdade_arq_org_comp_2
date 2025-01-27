from classesSimulador import *

# PROCESSOS GERAIS - CACHE E MEMORIA PRINCIPAL /////////////////////////////////////////////////////////////////////////////////////////////

def lerPalavra(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal, endereco: int, indiceProcCacheRequisitante: int) -> tuple[Palavra, list[str]]:

    arrayStrings = []

    # Cálculo de tag e índice da palavra a ser lida dentro da linha da cache

    palavrasPorLinha = conjuntoProcCaches.procCaches[indiceProcCacheRequisitante].palavrasPorLinha
    tag = endereco//palavrasPorLinha
    indicePalavra = endereco % palavrasPorLinha

    # Informa as informações de leitura

    arrayStrings.append(f"LEITURA: iniciando leitura\n")
    arrayStrings.append(f"do endereço {endereco}\n")
    arrayStrings.append(f"de tag {tag}\n")
    arrayStrings.append(f"requisitada pela cache {indiceProcCacheRequisitante + 1}\n\n")

    # Define a cache que requisita de acordo com o índice informado e busca a linha de acordo com a tag calculada

    procCacheRequisitante: ProcessadorCache = conjuntoProcCaches.procCaches[indiceProcCacheRequisitante]
    linhaComTagCorrespondente: LinhaCache = buscaLinhaCache(procCacheRequisitante, tag)

    # Se encontrou a linha na cache requisitante
    if linhaComTagCorrespondente != None:

        # Se a linha encontrada na cache requisitante tem estado MESIF diferente de inválido
        if linhaComTagCorrespondente.estadoMesif in (EstadoMesif.MODIFIED, EstadoMesif.EXCLUSIVE, EstadoMesif.FORWARD, EstadoMesif.SHARED):

            # Cache hit: retornar a palavra da linha da cache requisitante
            # de acordo com o seu índice
            # TODO: Exibir Cache Hit
            arrayStrings.append(f'''            CACHE: Hit de Leitura\n''')
            palavraLida = linhaComTagCorrespondente.palavras[indicePalavra]
            arrayStrings.append(f'''                    palavra lida: {palavraLida.conteudo}\n\n\n''')
            return palavraLida, arrayStrings
    
    # Se não saiu da função pelo return, então significa que não houve Cache Hit, logo deve-se
    # procurar em outras caches

    arrayStrings.append(f'''            CACHE: Miss de Leitura\n''')
    encontrouLinhaEmOutraCache, linhasEncontradasEmOutrasCaches, indicesProcCachesOutrasLinhas = buscaLinhaEmOutrasCaches(conjuntoProcCaches, tag, indiceProcCacheRequisitante)
    
    # linhasEncontradasEmOutrasCaches contém todas as linhas de outras caches com a mesma tag
    # a tarefa agora é verificar, dentre estas linhas, se há uma linha exclusiva, modificada,
    # ou forward

    estadoNaOutraCache = EstadoMesif.NOTFOUND
    for linha in linhasEncontradasEmOutrasCaches:
    
        if linha.estadoMesif in (EstadoMesif.EXCLUSIVE, EstadoMesif.MODIFIED, EstadoMesif.FORWARD):

            estadoNaOutraCache = linha.estadoMesif
            linhaEncontradaEmOutraCache = linha
    
    # Se terminou a procura em outras caches tendo encontrado a linha com estado diferente de inválido
    if estadoNaOutraCache in (EstadoMesif.EXCLUSIVE, EstadoMesif.MODIFIED, EstadoMesif.FORWARD):

        # Se não havia encontrado linha na cache requisitante (substituir uma linha existente ou adicionar linha)
        if linhaComTagCorrespondente == None:

            # Obtém qual linha será substituída
            linhaSubstituicao: LinhaCache = procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao]

            # Trata a substituição da linha que será substituída
            # Isto é, toma as devidas providências caso a linha esteja em estado forward ou modificado
            # (ver comentários na função trataExclusao)
            trataExclusao(linhaSubstituicao, conjuntoProcCaches, memoriaPrincipal, indiceProcCacheRequisitante, arrayStrings)

            # Transfere as palavras da linha da outra cache para a linha da cache requisitante - a que acabou-se de substituir
            # Além disso, faz a lógica de qual linha ficará no estado forward
            # (ver comentários na função transfereLinhaLeitura)
            transfereLinhaLeitura(linhaEncontradaEmOutraCache, linhaSubstituicao, procCacheRequisitante.palavrasPorLinha, memoriaPrincipal, endereco, arrayStrings)

            # Obtém a palavra do endereço desejado de acordo com o índice previamente calculado
            palavraLida = linhaSubstituicao.palavras[indicePalavra]

            # Atualiza o índice de substituição para manter a lógica de substituição FIFO
            atualizaIndiceDeSubstituicao(procCacheRequisitante)

        # Se havia encontrado uma linha na cache requisitante, porém esta linha estava em estado inválido
        else:

            # Transfere as palavras da linha da outra cache para a linha da cache requisitante - a que acabou-se de substituir
            # Além disso, faz a lógica de qual linha ficará no estado forward
            # (ver comentários na função transfereLinhaLeitura)
            transfereLinhaLeitura(linhaEncontradaEmOutraCache, linhaComTagCorrespondente, procCacheRequisitante.palavrasPorLinha, memoriaPrincipal, endereco, arrayStrings)

            # Obtém a palavra do endereço desejado de acordo com o índice previamente calculado
            palavraLida = linhaComTagCorrespondente.palavras[indicePalavra]
        
    else:
        # Se não encontrou na cache requisitante nem em outras caches
        # Leitura à memória
        
        # Se não havia encontrado linha na cache requisitante (substituir uma linha existente ou adicionar linha)
        if linhaComTagCorrespondente == None:

            # Obtém qual linha será substituída
            linhaSubstituicao = procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao]
            
            # Trata a substituição da linha que será substituída
            # Isto é, toma as devidas providências caso a linha esteja em estado forward ou modificado
            # (ver comentários na função trataExclusao)
            trataExclusao(linhaSubstituicao, conjuntoProcCaches, memoriaPrincipal, indiceProcCacheRequisitante, arrayStrings)

            # Necessária leitura à memória principal, já que 
            arrayStrings.append(f'''            MEMÓRIA PRINCIPAL: Leitura\n\n''')
            transfereBlocoParaLinha(memoriaPrincipal, endereco, linhaSubstituicao, procCacheRequisitante.palavrasPorLinha)
            
            palavraLida = linhaSubstituicao.palavras[indicePalavra]

            atualizaIndiceDeSubstituicao(procCacheRequisitante)
        
        # Se havia encontrado uma linha na cache requisitante, porém esta linha estava em estado inválido
        else:

            arrayStrings.append(f'''            MEMÓRIA PRINCIPAL: Leitura\n\n''')
            transfereBlocoParaLinha(memoriaPrincipal, endereco, linhaComTagCorrespondente, procCacheRequisitante.palavrasPorLinha)
            
            palavraLida = linhaComTagCorrespondente.palavras[indicePalavra]
    
    arrayStrings.append(f'''                     palavra lida: {palavraLida.conteudo}\n\n\n''')

    return palavraLida, arrayStrings

def escreverPalavra(conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal, endereco: int, indiceProcCacheRequisitante:int, conteudoNovaPalavra: int):

    arrayStrings = []

    novaPalavra = Palavra(Intervalo(0,1))
    novaPalavra.conteudo = conteudoNovaPalavra
    novaPalavra.sendoUsada = True
        

    # Cálculo de tag e índice da palavra a ser lida dentro da linha da cache

    palavrasPorLinha = conjuntoProcCaches.procCaches[indiceProcCacheRequisitante].palavrasPorLinha
    tag = endereco//palavrasPorLinha
    indicePalavra = endereco % palavrasPorLinha

    arrayStrings.append(f"ESCRITA: iniciando escrita\n")
    arrayStrings.append(f"do endereço {endereco}\n")
    arrayStrings.append(f"de tag {tag}\n")
    arrayStrings.append(f"requisitada pela cache {indiceProcCacheRequisitante + 1}\n\n")

    procCacheRequisitante = conjuntoProcCaches.procCaches[indiceProcCacheRequisitante]
    linhaComTagCorrespondente = buscaLinhaCache(procCacheRequisitante, tag)

    encontrouLinhaEmOutraCache, linhasEncontradasEmOutrasCaches, indicesProcCachesOutrasLinhas = buscaLinhaEmOutrasCaches(conjuntoProcCaches, tag, indiceProcCacheRequisitante)

    # Seta ocorreuWriteMiss para True. Porém, caso não tenha ocorrido,
    # será setado para False
    ocorreuWriteMiss = True

    # Se econtrou a linha na cache requisitante
    if linhaComTagCorrespondente != None:

        if linhaComTagCorrespondente.estadoMesif != EstadoMesif.INVALID:

            arrayStrings.append(f"            CACHE: Hit de Escrita\n")
            
            # Escrevendo a palavra de fato na cache
            linhaComTagCorrespondente.palavras[indicePalavra] = novaPalavra

            for linha in linhasEncontradasEmOutrasCaches:

                trataExclusao(linha, conjuntoProcCaches, memoriaPrincipal, indiceProcCacheRequisitante, arrayStrings)
                linha.estadoMesif = EstadoMesif.INVALID

            ocorreuWriteMiss = False

        linhaComTagCorrespondente.estadoMesif = EstadoMesif.MODIFIED
        linhaComTagCorrespondente.sendoUsada = True

    if ocorreuWriteMiss:

        estadoNaOutraCache = EstadoMesif.NOTFOUND
        for linha in linhasEncontradasEmOutrasCaches:
        
            if linha.estadoMesif in (EstadoMesif.EXCLUSIVE, EstadoMesif.MODIFIED, EstadoMesif.FORWARD):

                estadoNaOutraCache = linha.estadoMesif
                linhaEncontradaEmOutraCache = linha

        arrayStrings.append("            CACHE: Miss de Escrita\n")

        if estadoNaOutraCache in (EstadoMesif.EXCLUSIVE, EstadoMesif.MODIFIED, EstadoMesif.FORWARD):

            if linhaComTagCorrespondente == None:
                
                linhaSubstituicao = procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao]

                trataExclusao(linhaSubstituicao, conjuntoProcCaches, memoriaPrincipal, indiceProcCacheRequisitante, arrayStrings)

                transfereLinhaEscrita(linhaEncontradaEmOutraCache, linhaSubstituicao, procCacheRequisitante.palavrasPorLinha, memoriaPrincipal, endereco, arrayStrings, conjuntoProcCaches, indiceProcCacheRequisitante)

                linhaSubstituicao.palavras[indicePalavra] = novaPalavra

                atualizaIndiceDeSubstituicao(procCacheRequisitante)

                for linha in linhasEncontradasEmOutrasCaches:

                    trataExclusao(linha, conjuntoProcCaches, memoriaPrincipal, indiceProcCacheRequisitante, arrayStrings)
                    linha.estadoMesif = EstadoMesif.INVALID
            
            else:

                transfereLinhaEscrita(linhaEncontradaEmOutraCache, linhaComTagCorrespondente, procCacheRequisitante.palavrasPorLinha, memoriaPrincipal, endereco, arrayStrings, conjuntoProcCaches, indiceProcCacheRequisitante)

                linhaComTagCorrespondente.palavras[indicePalavra] = novaPalavra
            
            for linha in linhasEncontradasEmOutrasCaches:

                trataExclusao(linha, conjuntoProcCaches, memoriaPrincipal, indiceProcCacheRequisitante, arrayStrings)
                linha.estadoMesif = EstadoMesif.INVALID
        
        else:

            if linhaComTagCorrespondente == None:

                linhaSubstituicao = procCacheRequisitante.linhas[procCacheRequisitante.indiceSubstituicao]

                trataExclusao(linhaSubstituicao, conjuntoProcCaches, memoriaPrincipal, indiceProcCacheRequisitante, arrayStrings)

                arrayStrings.append(f'''            MEMÓRIA PRINCIPAL: Leitura\n\n''')
                transfereBlocoParaLinha(memoriaPrincipal, endereco, linhaSubstituicao, procCacheRequisitante.palavrasPorLinha)

                linhaSubstituicao.palavras[indicePalavra] = novaPalavra

                linhaSubstituicao.estadoMesif = EstadoMesif.MODIFIED
                linhaSubstituicao.tag = tag
                linhaSubstituicao.sendoUsada = True

                atualizaIndiceDeSubstituicao(procCacheRequisitante)
            
            else:

                arrayStrings.append(f'''            MEMÓRIA PRINCIPAL: Leitura\n\n''')
                transfereBlocoParaLinha(memoriaPrincipal, endereco, linhaComTagCorrespondente, procCacheRequisitante.palavrasPorLinha)

                linhaComTagCorrespondente.palavras[indicePalavra] = novaPalavra
    
    arrayStrings.append(f"                     palavra escrita: {novaPalavra.conteudo}\n\n\n")

    return arrayStrings

def transfereBlocoParaLinha(memoriaPrincipal, endereco, linha: LinhaCache, tamanhoLinha):
    
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

        encontrou = procCache.linhas[indiceLinhaCacheAtual].tag == tag
        
        if not encontrou:
        
            indiceLinhaCacheAtual += 1
    
    if encontrou:
        
        return procCache.linhas[indiceLinhaCacheAtual]
    
    else:
    
        return None

def buscaLinhaEmOutrasCaches(conjuntoProcCaches: ConjuntoProcessadoresCaches, tag: int, indiceProcCacheRequisitante: int) -> tuple[bool, list[LinhaCache], int]:

    indiceProcCacheAtual = 0
    encontrouLinhaEmOutraCache = False
    indicesProcCaches = []
    linhasEncontradasEmOutrasCaches = []
    while indiceProcCacheAtual < conjuntoProcCaches.quantidadeProcCaches:

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

def transfereLinhaLeitura(linhaEncontradaEmOutraCache: LinhaCache, linhaCacheRequisitante: LinhaCache, tamanhoLinha, memoriaPrincipal, endereco, arrayStrings: list[str]):
    
    copiaLinha(linhaEncontradaEmOutraCache, linhaCacheRequisitante, tamanhoLinha)

    if linhaEncontradaEmOutraCache.estadoMesif == EstadoMesif.FORWARD:

        linhaCacheRequisitante.estadoMesif = EstadoMesif.SHARED
    else:

        if linhaEncontradaEmOutraCache.estadoMesif == EstadoMesif.MODIFIED:

            arrayStrings.append(f'''            MEMÓRIA PRINCIPAL: Escrita\n\n''')
            escreverBlocoMemoriaPrincipal(memoriaPrincipal, endereco, linhaEncontradaEmOutraCache.palavras)
        
        linhaCacheRequisitante.estadoMesif = EstadoMesif.FORWARD
    
        linhaEncontradaEmOutraCache.estadoMesif = EstadoMesif.SHARED

def transfereLinhaEscrita(linhaEncontradaEmOutraCache: LinhaCache, linhaCacheRequisitante: LinhaCache, tamanhoLinha, memoriaPrincipal, endereco, arrayStrings: list[str], conjuntoProcCaches, indiceProcCacheRequisitante):

    copiaLinha(linhaEncontradaEmOutraCache, linhaCacheRequisitante, tamanhoLinha)

    if linhaEncontradaEmOutraCache.estadoMesif == EstadoMesif.MODIFIED:

        arrayStrings.append(f'''            MEMÓRIA PRINCIPAL: Escrita\n\n''')
        escreverBlocoMemoriaPrincipal(memoriaPrincipal, endereco, linhaEncontradaEmOutraCache.palavras)
    
    trataExclusao(linhaEncontradaEmOutraCache, conjuntoProcCaches, memoriaPrincipal, indiceProcCacheRequisitante, arrayStrings)
    linhaEncontradaEmOutraCache.estadoMesif = EstadoMesif.INVALID
    linhaCacheRequisitante.estadoMesif = EstadoMesif.MODIFIED

def trataExclusao(linhaSubstituicao: LinhaCache, conjuntoProcCaches: ConjuntoProcessadoresCaches, memoriaPrincipal: MemoriaPrincipal, indiceProcCacheRequisitante: int, arrayStrings: list[str]):

    if linhaSubstituicao.estadoMesif == EstadoMesif.MODIFIED:

        endereco = linhaSubstituicao.tag * memoriaPrincipal.palavrasPorBloco
        arrayStrings.append(f'''           MEMÓRIA PRINCIPAL: Escrita\n\n''')
        escreverBlocoMemoriaPrincipal(memoriaPrincipal, endereco, linhaSubstituicao.palavras)
    
    elif linhaSubstituicao.estadoMesif == EstadoMesif.FORWARD:

        trataLinhaExclusaoForward(linhaSubstituicao, conjuntoProcCaches, indiceProcCacheRequisitante)

def trataLinhaExclusaoForward(linhaSubstituicao: LinhaCache, conjuntoProcCaches: ConjuntoProcessadoresCaches, indiceProCacheRequisitante: int):

    encontrouLinhaEmOutrasCaches, linhasEncontradasEmOutrasCaches, indicesProcCaches = buscaLinhaEmOutrasCaches(conjuntoProcCaches, linhaSubstituicao.tag, indiceProCacheRequisitante)
    primeiraLinhaShared = None
    for linha in linhasEncontradasEmOutrasCaches:

        if (primeiraLinhaShared == None) and (linha.estadoMesif == EstadoMesif.SHARED):

            linha.estadoMesif = EstadoMesif.FORWARD
            primeiraLinhaShared = linha

# PROCESSOS MEMÓRIA PRINCIPAL //////////////////////////////////////////////////////////////////////////////////////////////////////////////

def lerBlocoMemoriaPrincipal(memoriaPrincipal: MemoriaPrincipal, endereco: int):

    #TODO: Exibir leitura na memória principal

    palavrasPorBloco = memoriaPrincipal.palavrasPorBloco
    indiceBloco = endereco//palavrasPorBloco

    return memoriaPrincipal.blocos[indiceBloco]

def escreverBlocoMemoriaPrincipal(memoriaPrincipal: MemoriaPrincipal, endereco: int, palavras):

    #TODO: Exibir escrita na memória principal

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

# OUTROS ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# def estadoMesifParaString(estadoMesif: EstadoMesif):
