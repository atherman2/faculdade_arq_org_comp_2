from controlaSimulador import *
from classesAplicacao import *
from customtkinter import *

class Operacao(Enum):

    CADASTRO = auto()
    CONSULTA = auto()
    EDITAR = auto()
    REMOVER = auto()

class Interface(CTk):

    def __init__(self, cjtoCaches: ConjuntoProcessadoresCaches, memPrinc: MemoriaPrincipal, gerProd: GerenciaProdutos):

        super().__init__()
        self.geometry("1280x540")
        self.title("Simulador de Coerência de Cache e Aplicação estilo Estoque de Mercado")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.cjtoCaches = cjtoCaches
        self.memPrinc = memPrinc
        self.gerProd = gerProd

        self.quantidadeInfoPorProduto = 4

        self.tamanhoMp = self.memPrinc.palavrasPorBloco * self.memPrinc.quantidadeDeBlocos
        self.intervaloEnderecoInfo = self.tamanhoMp//self.quantidadeInfoPorProduto
        self.gerProd.maximoProdutos = self.intervaloEnderecoInfo
        self.dicionarioExecutaOperacoes = {
            Operacao.CADASTRO: self.cadastraProdutoPorComando,
            Operacao.CONSULTA: self.consultaProdutoPorComando,
            Operacao.EDITAR: self.editaProdutoPorComando,
            Operacao.REMOVER : self.removeProdutoPorComando
        }

        self.framePrincipal = FrameComScroll(self)
        self.framePrincipal.grid(row=0, column=0, sticky="snew")

        self.framesCaches = [self.framePrincipal.frameEstadoCaches, self.framePrincipal.frameLogCaches]
        self.framesMp = [self.framePrincipal.frameEstadoMp, self.framePrincipal.frameLogMp]
        self.frameLogOp = [self.framePrincipal.frameLogOperacoes]

        self.informarEstadoInicial()
        self.indiceOperacao = 1

        frameMenu = self.framePrincipal.frameTesteMenu
        frameMenu.incluirBotaoSubframe("Cadastrar Produto", "Cadastrar", self.comunicaCadastro)
        frameMenu.incluirBotaoSubframe("Consultar Produto", "Consultar", self.comunicaConsulta)
        frameMenu.incluirBotaoSubframe("Editar Produto", "Editar", self.comunicaEdicao)
        frameMenu.incluirBotaoSubframe("Remover Produto", "Remover", self.comunicaConfirmacaoRemocao)

    def escrever(self, endereco, info):

        arrayStringsOperacao = escreverPalavra(self.cjtoCaches, self.memPrinc, endereco, self.indiceProcCache, info)
        
        self.informarOperacao()
        self.atualizarInfoEstadoCaches()
        self.atualizarInfoEstadoMp()
        self.atualizarLogOperacoes(arrayStringsOperacao)

    def escreverVetor(self, enderecoBase, vetorInfo):

        for indiceInfo, info in enumerate(vetorInfo):

            self.escrever(enderecoBase + indiceInfo * self.intervaloEnderecoInfo, info)
    
    def ler(self, endereco):

        palavraLida, arrayStringsOperacao = lerPalavra(self.cjtoCaches, self.memPrinc, endereco, self.indiceProcCache)

        self.informarOperacao()
        self.atualizarInfoEstadoCaches()
        self.atualizarInfoEstadoMp()
        self.atualizarLogOperacoes(arrayStringsOperacao)

        return palavraLida.conteudo

    def lerVetor(self, enderecoBase):

        vetorInfo = []

        for indiceInfo in range(self.quantidadeInfoPorProduto):

            vetorInfo.append(self.ler(enderecoBase + indiceInfo * self.intervaloEnderecoInfo))

        return vetorInfo

    def cadastroProdutoSilencioso(self, vetorProduto: list):

        enderecoBaseProduto = self.gerProd.adicionaProduto(vetorProduto[0])

        if enderecoBaseProduto in (-1, -2):

            return enderecoBaseProduto

        vetorInfo = vetorProduto[1:]
        vetorInfo.insert(1, self.indiceProcCache)
        self.escreverVetor(enderecoBaseProduto, vetorInfo)

        return vetorProduto
    
    def cadastraProdutoPorComando(self, vetorProduto):

        self.indiceProcCache = vetorProduto[-1]
        self.cadastroProdutoSilencioso(vetorProduto[:-1])

    def exibirCadastro(self, retornoAdiciona, nomeProduto):

        if retornoAdiciona == -1:

            JanelaProdutoJaExistente(self, nomeProduto)
        
        elif retornoAdiciona == -2:

            JanelaLimiteProdutos(self)

        else:

            JanelaOperacaoBemSucedida(self, "Cadastro")
    
    def comunicaCadastro(self):

        self.indiceProcCache = self.framePrincipal.frameTesteMenu.mercadoAtual
        vetorProduto = self.framePrincipal.frameTesteMenu.subFrames["Cadastrar Produto"].getParesCadastro()
        self.exibirCadastro(self.cadastroProdutoSilencioso(vetorProduto), vetorProduto[0])

    def consultaProdutoSilenciosa(self, stringProduto):

        enderecoBaseProduto = self.gerProd.consultaProduto(stringProduto)

        if enderecoBaseProduto != None:

            arrayProduto = self.lerVetor(enderecoBaseProduto)

            linhasConsulta = [f"Nome do Produto: {stringProduto}\n"]
            linhasConsulta += [f"Quantidade em estoque: {str(arrayProduto[0])}\n"]
            linhasConsulta += [f"Preço: {str(arrayProduto[2])}\n"]
            linhasConsulta += [f"Custo no fornecedor: {str(arrayProduto[3])}\n"]
            if self.indiceProcCache == arrayProduto[1]:

                linhasConsulta += [f"O produto se encontra no seu mercado! (Mercado {arrayProduto[1] + 1})"]
            
            else:

                linhasConsulta += [f"O produto encontra-se em outro mercado! (Mercado {arrayProduto[1] + 1})"]
        
        else:

            linhasConsulta = ["Produto não encontrado!\n"]

        return linhasConsulta
    
    def consultaProdutoPorComando(self, vetorProduto):

        self.indiceProcCache = vetorProduto[-1]
        self.consultarProduto(vetorProduto[:-1])

    def executaOperacoesPorComando(self, vetorOperacoes):

        for operacao in vetorOperacoes:

            self.dicionarioExecutaOperacoes[operacao[0]](operacao[1:])

    def exibirConsulta(self, linhasConsulta):
        
        if linhasConsulta == ["Produto não encontrado!\n"]:

            JanelaProdutoNaoEncontrado(self)

        else:
            
            self.janelaConsulta = JanelaExibirConsulta(self)
            self.janelaConsulta.adicionarLinhasTexto(linhasConsulta)
            self.janelaConsulta.adicionarFrameBotoes()
            self.janelaConsulta.frameBotoes.adicionarBotao("Ok", self.janelaConsulta.destroy)
    
    def consultarProduto(self, stringProduto):

        self.exibirConsulta(self.consultaProdutoSilenciosa(stringProduto))

    def comunicaConsulta(self):

        self.indiceProcCache = self.framePrincipal.frameTesteMenu.mercadoAtual
        stringProduto = self.framePrincipal.frameTesteMenu.subFrames["Consultar Produto"].getParesCadastro()[0]
        self.consultarProduto(stringProduto)

    def edicaoProdutoSilenciosa(self, vetorProduto: list):

        enderecoBaseProduto = self.gerProd.consultaProduto(vetorProduto[0])

        if enderecoBaseProduto == None:

            return None
        
        else:

            vetorInfo = vetorProduto[1:]
            vetorInfo.insert(1, self.indiceProcCache)
            self.escreverVetor(enderecoBaseProduto, vetorInfo)
            
            return vetorProduto
    
    def editaProdutoPorComando(self, vetorProduto):

        self.indiceProcCache = vetorProduto[-1]
        self.cadastroProdutoSilencioso(vetorProduto[:-1])

    def exibirEdicao(self, retornoEdita):

        if retornoEdita == None:

            JanelaProdutoNaoEncontrado(self)
        
        else:

            JanelaOperacaoBemSucedida(self, "Edição")

    def comunicaEdicao(self):

        self.indiceProcCache = self.framePrincipal.frameTesteMenu.mercadoAtual
        vetorProduto = self.framePrincipal.frameTesteMenu.subFrames["Editar Produto"].getParesCadastro()
        self.exibirEdicao(self.edicaoProdutoSilenciosa(vetorProduto))

    def consultaProdutoParaRemocaoSilenciosa(self, stringProduto):

        enderecoBaseProduto = self.gerProd.consultaProduto(stringProduto)

        if enderecoBaseProduto != None:

            arrayProduto = self.lerVetor(enderecoBaseProduto)

            linhasConsulta = [f"Nome do Produto: {stringProduto}\n"]
            linhasConsulta += [f"Quantidade em estoque: {str(arrayProduto[0])}\n"]
            linhasConsulta += [f"Preço: {str(arrayProduto[2])}\n"]
            linhasConsulta += [f"Custo no fornecedor: {str(arrayProduto[3])}\n"]
            if self.indiceProcCache == arrayProduto[1]:

                linhasConsulta += [f"O produto se encontra no seu mercado! (Mercado {arrayProduto[1] + 1})"]
            
            else:

                linhasConsulta += [f"O produto encontra-se em outro mercado! (Mercado {arrayProduto[1] + 1})"]
        
        else:

            linhasConsulta = ["Produto não encontrado!\n"]

        return linhasConsulta

    def exibirConfirmacaoRemocao(self, stringProduto, linhasInfoProduto):

        if linhasInfoProduto == ["Produto não encontrado!\n"]:

            JanelaProdutoNaoEncontrado(self)

        else:

            self.stringProdutoRemocao = stringProduto
            self.janelaRemocao = JanelaExibirRemocao(self, linhasInfoProduto)
            self.janelaRemocao.frameBotoes.adicionarBotao("Remover", self.removeProduto)

    def confirmacaoRemocaoProduto(self, stringProduto):

        self.exibirConfirmacaoRemocao(stringProduto, self.consultaProdutoParaRemocaoSilenciosa(stringProduto))

    def comunicaConfirmacaoRemocao(self):

        self.indiceProcCache = self.framePrincipal.frameTesteMenu.mercadoAtual
        stringProduto =  self.framePrincipal.frameTesteMenu.subFrames["Remover Produto"].getParesCadastro()[0]
        self.confirmacaoRemocaoProduto(stringProduto)

    def removeProduto(self):

        self.gerProd.removeProduto(self.stringProdutoRemocao)
        self.janelaRemocao.destroy()
        self.janelaSucessoRemocao = JanelaOperacaoBemSucedida(self, "Remoção")

    def removeProdutoPorComando(self, vetorProduto):

        self.indiceProcCache = vetorProduto[-1]
        retornoConsulta = self.consultaProdutoParaRemocaoSilenciosa(self, vetorProduto[0])
        if retornoConsulta != ["Produto não encontrado!\n"]:

            self.gerProd.removeProduto(vetorProduto[0])

    def atualizarInfoEstadoCaches(self):

        cjtoCachesArrayStrings = self.cjtoCaches.paraArrayStrings()

        self.framePrincipal.frameEstadoCaches.limparTexto()
        self.framePrincipal.frameEstadoCaches.adicionarLinhasTexto(cjtoCachesArrayStrings)

        self.framePrincipal.frameLogCaches.adicionarLinhasTexto(cjtoCachesArrayStrings)
    
    def atualizarInfoEstadoMp(self):

        memPrincArrayStrings = self.memPrinc.paraArrayStrings()

        self.framePrincipal.frameEstadoMp.limparTexto()
        self.framePrincipal.frameEstadoMp.adicionarLinhasTexto(memPrincArrayStrings)

        self.framePrincipal.frameLogMp.adicionarLinhasTexto(memPrincArrayStrings)
    
    def atualizarLogOperacoes(self, arrayStringsOperacao):

        self.framePrincipal.frameLogOperacoes.adicionarLinhasTexto(arrayStringsOperacao)
    
    def broadCastLinhasTexto(self, linhasTexto):

        for frame in (self.framesCaches + self.framesMp + self.frameLogOp):

            frame.adicionarLinhasTexto(linhasTexto)
    
    def informarEstadoInicial(self):

        estadoInicial = [f"ESTADO INICIAL:\n\n"]
        
        for frame in (self.framesCaches + self.framesMp):

            frame.adicionarLinhasTexto(estadoInicial)

        self.atualizarInfoEstadoCaches()
        self.atualizarInfoEstadoMp()

    def informarOperacao(self):

        self.broadCastLinhasTexto([f"\n\n\nOPERAÇÃO #{self.indiceOperacao}\n\n"])
        self.indiceOperacao += 1

class FrameComScroll(CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frameTesteMenu = FrameComMenu(self)
        self.frameTesteMenu.grid(row=0, column=0, padx=10, pady=10, sticky="snew")

        self.frameTesteMenu.incluirTitulo("Menu do Mercado")

        self.frameLogOperacoes = FrameComTexto(self)
        self.frameLogOperacoes.grid(row=1, column=0, padx=10, pady=10, sticky="snew")

        self.frameLogOperacoes.incluirTitulo("Log de Operações")
        self.frameLogOperacoes.incluirTexto()

        self.frameEstadoCaches = FrameComTexto(self)
        self.frameEstadoCaches.grid(row=0, column=1, padx=10, pady=10, sticky="snew")

        self.frameEstadoCaches.incluirTitulo("Estado Atual da Cache")
        self.frameEstadoCaches.incluirTexto()

        self.frameLogCaches = FrameComTexto(self)
        self.frameLogCaches.grid(row=1, column=1, padx=10, pady=10, sticky="snew")

        self.frameLogCaches.incluirTitulo("Histórico das Caches")
        self.frameLogCaches.incluirTexto()
        
        self.frameLogCaches.configure(height=460)
        self.frameLogCaches.texto.configure(height=340)

        self.frameEstadoMp = FrameComTexto(self)
        self.frameEstadoMp.grid(row=0, column=2, padx=10, pady=10, sticky="snew")

        self.frameEstadoMp.incluirTitulo("Estado Atual da Memória Principal")
        self.frameEstadoMp.incluirTexto()

        self.frameLogMp = FrameComTexto(self)
        self.frameLogMp.grid(row=1, column=2, padx=10, pady=10, sticky="snew")

        self.frameLogMp.incluirTitulo("Histórico das Caches")
        self.frameLogMp.incluirTexto()
        
        self.frameLogMp.configure(height=460)
        self.frameLogMp.texto.configure(height=340)

class FrameComTexto(CTkFrame):
    
    def __init__(self, master):

        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
    def incluirTitulo(self, titulo):

        self.titulo =  CTkLabel(self, text=titulo)
        self.titulo.grid(row=0, column=0, pady=(10,5), padx=10)

    def incluirTexto(self):

        self.texto = CTkTextbox(self)
        self.texto.grid(row=1, column=0, sticky="snew", pady=5,padx=10)
        self.texto.configure(state="disabled")
    
    def adicionarLinhasTexto(self, linhasTexto):

        self.texto.configure(state="normal")
        for linhaTexto in linhasTexto:
            self.texto.insert(END, linhaTexto)
        self.texto.configure(state="disabled")
        self.texto.see(END)
    
    def limparTexto(self):
        self.texto.configure(state="normal")
        self.texto.delete("1.0", END)
        self.texto.configure(state="disabled")

class FrameComMenu(CTkFrame):

    def __init__(self, master):

        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.mercadoAtual = 0

        self.opcoesQualMercado = ["Mercado 1", "Mercado 2", "Mercado 3", "Mercado 4"]
        self.menuQualMercado = CTkOptionMenu(self, values=self.opcoesQualMercado, command=self.alternarMercado)
        self.menuQualMercado.set("Mercado 1")
        self.menuQualMercado.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        self.opcoesSubFrame = ["Cadastrar Produto", "Consultar Produto", "Editar Produto", "Remover Produto"]
        self.menuSubFrame = CTkOptionMenu(self, values=self.opcoesSubFrame, command=self.alternarSubframeAtual)
        self.menuSubFrame.set("Cadastrar Produto")
        self.menuSubFrame.grid(row=2, column=0, padx=10, pady=10, sticky="new")

        self.subFrames: dict[(str, FrameComEntradas)] = {
            "Cadastrar Produto": criaSubFrameCadastro(self),
            "Consultar Produto": criaSubFrameConsulta(self),
            "Editar Produto": criaSubFrameEditar(self),
            "Remover Produto": criaSubFrameRemover(self)
        }

        self.subFrames["Cadastrar Produto"].grid(row=3, column=0, padx=20, pady=20, sticky="snew")
        self.subFrameAtual = "Cadastrar Produto"

    def incluirTitulo(self, titulo):

        self.titulo =  CTkLabel(self, text=titulo)
        self.titulo.grid(row=0, column=0, pady=(10,5), padx=10)
    
    def alternarSubframeAtual(self, opcao):

        self.subFrames[self.subFrameAtual].grid_forget()
        self.subFrames[opcao].grid(row=3, column=0, padx=20, pady=20, sticky="snew")
        self.subFrameAtual = opcao
    
    def incluirBotaoSubframe(self, stringSubframe, textoBotao, acaoBotao):

        self.subFrames[stringSubframe].incluirBotao(textoBotao, acaoBotao)
    
    def alternarMercado(self, stringNovoMercado: str):

        self.mercadoAtual = int(stringNovoMercado.split(" ")[1]) - 1

class FrameComEntradas(CTkFrame):
    
    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        
        self.subFramesParCadastro: list[SubFrameParCadastro] = []

        self.indiceComponent = 1
    
    def incluirTitulo(self, titulo):

        self.titulo = CTkLabel(self, text=titulo)
        self.titulo.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,5))
    
    def incluirPainelInformações(self):

        self.grid_rowconfigure(self.indiceComponent, weight=1)

        self.frameExibirInfo = FrameComTexto(self)
        self.frameExibirInfo.grid(row=self.indiceComponent, column=0, padx=10, pady=(10,5), sticky="snew")

        self.frameExibirInfo.incluirTitulo("Informações Cadastradas")
        self.frameExibirInfo.incluirTexto()
        self.frameExibirInfo.incluirBotao("Exibir", self.exibirInfo)

        self.indiceComponent += 1

    def adicionarSubFrameParCadastro(self):

        self.subFramesParCadastro.append(SubFrameParCadastro(self))
        self.subFramesParCadastro[-1].grid(row=self.indiceComponent, column=0, sticky="ew")
        self.indiceComponent += 1
    
    def getParesCadastro(self):

        retorno = []
        for subFrameParCadastro in self.subFramesParCadastro:
            variavelEntrada: StringVar = subFrameParCadastro.variavelEntrada
            retorno.append(variavelEntrada.get())
        return retorno

    def incluirBotao(self, textoBotao, acaoBotao):

        self.botaoCadastrar = CTkButton(self, text=textoBotao, command=acaoBotao)
        self.botaoCadastrar.grid(row=self.indiceComponent, column=0, sticky="ew")
        self.indiceComponent += 1

class SubFrameParCadastro(CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure(1, weight=1)
    
    def incluirRotulo(self, rotulo):

        self.rotulo = CTkLabel(self, text=rotulo)
        self.rotulo.grid(row=0, column=0, padx=(10,5), pady=10, sticky="snew")

    def incluirEntrada(self, indice):

        self.variavelEntrada = StringVar(master=self, name=f"variavelEntrada{indice}")
        self.entrada = CTkEntry(master=self, textvariable=self.variavelEntrada)
        self.entrada.grid(row=0, column=1, padx=(5,10), pady=10, sticky="snew")

def criaSubFrameCadastro(framePai: FrameComMenu):

    subFrameCadastro = FrameComEntradas(framePai)
    subFrameCadastro.incluirTitulo("Cadastrar Produto")

    indiceSubFrameParCadastro = 0

    subFrameCadastro.adicionarSubFrameParCadastro()
    subFrameCadastro.subFramesParCadastro[indiceSubFrameParCadastro].incluirRotulo("Nome do\nproduto:")
    subFrameCadastro.subFramesParCadastro[indiceSubFrameParCadastro].incluirEntrada(indiceSubFrameParCadastro)

    indiceSubFrameParCadastro += 1

    subFrameCadastro.adicionarSubFrameParCadastro()
    subFrameCadastro.subFramesParCadastro[indiceSubFrameParCadastro].incluirRotulo("Quantidade\nem estoque:")
    subFrameCadastro.subFramesParCadastro[indiceSubFrameParCadastro].incluirEntrada(indiceSubFrameParCadastro)

    indiceSubFrameParCadastro += 1

    subFrameCadastro.adicionarSubFrameParCadastro()
    subFrameCadastro.subFramesParCadastro[indiceSubFrameParCadastro].incluirRotulo("Preço:")
    subFrameCadastro.subFramesParCadastro[indiceSubFrameParCadastro].incluirEntrada(indiceSubFrameParCadastro)

    indiceSubFrameParCadastro += 1

    subFrameCadastro.adicionarSubFrameParCadastro()
    subFrameCadastro.subFramesParCadastro[indiceSubFrameParCadastro].incluirRotulo("Custo\nno fornecedor:")
    subFrameCadastro.subFramesParCadastro[indiceSubFrameParCadastro].incluirEntrada(indiceSubFrameParCadastro)

    return subFrameCadastro

def criaSubFrameConsulta(framePai: FrameComMenu):

    subFrameConsulta =  FrameComEntradas(framePai)
    subFrameConsulta.incluirTitulo("Consultar Produto")

    indiceEntradas = 0

    subFrameConsulta.adicionarSubFrameParCadastro()
    subFrameConsulta.subFramesParCadastro[indiceEntradas].incluirRotulo("Nome do\nProduto:")
    subFrameConsulta.subFramesParCadastro[indiceEntradas].incluirEntrada(indiceEntradas)

    return subFrameConsulta

def criaSubFrameEditar(framePai: FrameComMenu):

    subFrameEditar = FrameComEntradas(framePai)
    subFrameEditar.incluirTitulo("Editar Produto")

    indiceEntradas = 0

    subFrameEditar.adicionarSubFrameParCadastro()
    subFrameEditar.subFramesParCadastro[indiceEntradas].incluirRotulo("Nome do\nProduto:")
    subFrameEditar.subFramesParCadastro[indiceEntradas].incluirEntrada(indiceEntradas)

    indiceEntradas += 1
    
    subFrameEditar.adicionarSubFrameParCadastro()
    subFrameEditar.subFramesParCadastro[indiceEntradas].incluirRotulo("Quantidade\nem estoque:")
    subFrameEditar.subFramesParCadastro[indiceEntradas].incluirEntrada(indiceEntradas)

    indiceEntradas += 1
    
    subFrameEditar.adicionarSubFrameParCadastro()
    subFrameEditar.subFramesParCadastro[indiceEntradas].incluirRotulo("Custo\nno fornecedor:")
    subFrameEditar.subFramesParCadastro[indiceEntradas].incluirEntrada(indiceEntradas)

    indiceEntradas += 1
    
    subFrameEditar.adicionarSubFrameParCadastro()
    subFrameEditar.subFramesParCadastro[indiceEntradas].incluirRotulo("Preço:")
    subFrameEditar.subFramesParCadastro[indiceEntradas].incluirEntrada(indiceEntradas)

    return subFrameEditar

def criaSubFrameRemover(framePai: FrameComMenu):

    subFrameRemover = FrameComEntradas(framePai)
    subFrameRemover.incluirTitulo("Remover Produto")

    indiceEntradas = 0

    subFrameRemover.adicionarSubFrameParCadastro()
    subFrameRemover.subFramesParCadastro[indiceEntradas].incluirRotulo("Nome do\nProduto:")
    subFrameRemover.subFramesParCadastro[indiceEntradas].incluirEntrada(indiceEntradas)

    return subFrameRemover

class JanelaSecundaria(CTkToplevel):

    def __init__(self, pai):

        super().__init__(pai)
        self.geometry("300x380")
        self.grab_set()
        self.grid_columnconfigure(0, weight=1)
        self.indiceComponentes = 0
    
    def setTitulo(self, titulo):

        self.title(titulo)
    
    def adicionarRotulo(self, rotulo):

        self.rotulo = CTkLabel(self, text=rotulo)
        self.rotulo.grid(row=self.indiceComponentes, column=0, padx=15, pady=15, sticky="ew")
        self.grid_columnconfigure(self.indiceComponentes, weight=1)
        self.indiceComponentes += 1

    def incluirFrameTexto(self):
        
        self.frameTexto = FrameComTexto(self)
        self.frameTexto.incluirTexto()
        self.frameTexto.grid(row=self.indiceComponentes, column=0, padx=15, pady=15, sticky="snew")
        
        self.indiceComponentes += 1

    def adicionarLinhasTexto(self, linhasTexto):

        self.frameTexto.adicionarLinhasTexto(linhasTexto)
    
    def adicionarFrameBotoes(self):

        self.frameBotoes = FrameBotoesAddHorizontal(self)
        self.frameBotoes.grid(row=self.indiceComponentes, column=0, padx=15, pady=15, sticky="ew")
        
        self.indiceComponentes += 1

class JanelaProdutoJaExistente(JanelaSecundaria):

    def __init__(self, pai, nomeProduto):

        super().__init__(pai)
        self.setTitulo("Erro")
        self.adicionarRotulo(f"Produto {nomeProduto} que tenta-se cadastrar\njá está cadastrado!")
        self.adicionarFrameBotoes()
        self.frameBotoes.adicionarBotao("Ok", self.destroy)

class JanelaLimiteProdutos(JanelaSecundaria):

    def __init__(self, pai):

        super().__init__(pai)
        self.setTitulo("Erro")
        self.adicionarRotulo("Máximo de produtos atingido!")
        self.adicionarFrameBotoes()
        self.frameBotoes.adicionarBotao("Ok", self.destroy)

class JanelaExibirConsulta(JanelaSecundaria):

    def __init__(self, pai):

        super().__init__(pai)
        self.setTitulo("Consulta de Produto")
        self.adicionarRotulo("Exibição do Produto Consultado")
        self.incluirFrameTexto()

class JanelaExibirRemocao(JanelaSecundaria):

    def __init__(self, pai, linhasInfoProduto):

        super().__init__(pai)
        self.setTitulo("Remoção de Produto")
        self.adicionarRotulo("Deseja remover este produto?")
        self.incluirFrameTexto()
        self.adicionarLinhasTexto(linhasInfoProduto)
        self.adicionarFrameBotoes()
        self.frameBotoes.adicionarBotao("Cancelar", self.destroy)

class JanelaProdutoNaoEncontrado(JanelaSecundaria):

    def __init__(self, pai):

        super().__init__(pai)
        self.setTitulo("Erro")
        self.adicionarRotulo("Produto não encontrado!")
        self.adicionarFrameBotoes()
        self.frameBotoes.adicionarBotao("Ok", self.destroy)

class JanelaOperacaoBemSucedida(JanelaSecundaria):

    def __init__(self, pai, nomeOperacao):

        super().__init__(pai)
        self.setTitulo("Sucesso")
        self.adicionarRotulo(f"{nomeOperacao} concluiu-se com sucesso!")
        self.adicionarFrameBotoes()
        self.frameBotoes.adicionarBotao("Ok", self.destroy)

class FrameBotoesAddHorizontal(CTkFrame):

    def __init__(self, pai):

        super().__init__(pai)
        self.indiceBotao = 0
        self.botoes: list[CTkButton] = []
        self.grid_rowconfigure(0, weight=1)
    
    def adicionarBotao(self, textoBotao, acaoBotao):

        self.grid_columnconfigure(self.indiceBotao, weight=1)
        self.botoes.append(CTkButton(self, text=textoBotao, command=acaoBotao))
        self.botoes[self.indiceBotao].grid(row=0, column=self.indiceBotao, padx=15, pady=15)
        
        self.indiceBotao += 1

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
    
    gerenciaProdutos = GerenciaProdutos()

    interface = Interface(conjuntoProcCaches, memoriaPrincipal, gerenciaProdutos)
    interface.mainloop()
