from manipulaEntidades import *
from customtkinter import *

class Interface(CTk):

    def __init__(self, cjtoCaches: ConjuntoProcessadoresCaches, memPrinc: MemoriaPrincipal):

        super().__init__()
        self.geometry("1280x540")
        self.title("Simulador de Coerência de Cache e Aplicação estilo Estoque de Mercado")

        self.cjtoCaches = cjtoCaches
        self.memPrinc = memPrinc

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

        self.frameEstadoCache = FrameComTexto(self)
        self.frameEstadoCache.grid(row=0, column=1, padx=10, pady=10, sticky="snew")

        self.frameEstadoCache.incluirTitulo("Estado Atual da Cache")
        self.frameEstadoCache.incluirTexto()

        self.frameLogCaches = FrameComTexto(self)
        self.frameLogCaches.grid(row=1, column=1, padx=10, pady=10, sticky="snew")

        self.frameLogCaches.incluirTitulo("Histórico das Caches")
        self.frameLogCaches.incluirTexto()

        self.frameEstadoMP = FrameComTexto(self)
        self.frameEstadoMP.grid(row=0, column=2, padx=10, pady=10, sticky="snew")

        self.frameEstadoMP.incluirTitulo("Estado Atual da Memória Principal")
        self.frameEstadoMP.incluirTexto()

        self.frameLogMP = FrameComTexto(self)
        self.frameLogMP.grid(row=1, column=2, padx=10, pady=10, sticky="snew")

        self.frameLogMP.incluirTitulo("Histórico das Caches")
        self.frameLogMP.incluirTexto()

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

        self.opcoes = ["Cadastrar Produto", "Consultar Produto", "Editar Produto", "Remover Produto"]
        self.menu = CTkOptionMenu(self, values=self.opcoes)
        self.menu.set("Cadastrar Produto")
        self.menu.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        self.subFrameCadastro = criaSubFrameCadastro(self)
        self.subFrameCadastro.grid(row=2, column=0, padx=20, pady=20, sticky="snew")

    def incluirTitulo(self, titulo):

        self.titulo =  CTkLabel(self, text=titulo)
        self.titulo.grid(row=0, column=0, pady=(10,5), padx=10)


class FrameComEntradas(CTkFrame):
    
    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        
        self.subFramesParCadastro: list[SubFrameParCadastro] = []

        self.itensCadastrados = []

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
    
    def getParesCadastros(self):

        retorno = []
        for subFrameParCadastro in self.subFramesParCadastro:
            variavelEntrada: StringVar = subFrameParCadastro.variavelEntrada
            retorno.append(variavelEntrada.get())
        return retorno
    
    def cadastrar(self):

        self.itensCadastrados.append(self.getParesCadastros())

    def incluirBotaoCadastrar(self):

        self.botaoCadastrar = CTkButton(self, text="Cadastrar", command=self.cadastrar)
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

def criaSubFrameCadastro(frame: FrameComMenu):

    subFrameCadastro = FrameComEntradas(frame)
    subFrameCadastro.incluirTitulo("Cadastrar Produto")

    subFrameCadastro.adicionarSubFrameParCadastro()
    subFrameCadastro.subFramesParCadastro[0].incluirRotulo("Quantidade\nem estoque:")
    subFrameCadastro.subFramesParCadastro[0].incluirEntrada(0)
    subFrameCadastro.adicionarSubFrameParCadastro()
    subFrameCadastro.subFramesParCadastro[1].incluirRotulo("Preço:")
    subFrameCadastro.subFramesParCadastro[1].incluirEntrada(1)
    subFrameCadastro.adicionarSubFrameParCadastro()
    subFrameCadastro.subFramesParCadastro[2].incluirRotulo("Mercado:")
    subFrameCadastro.subFramesParCadastro[2].incluirEntrada(2)
    subFrameCadastro.adicionarSubFrameParCadastro()
    subFrameCadastro.subFramesParCadastro[3].incluirRotulo("Custo\nno fornecedor:")
    subFrameCadastro.subFramesParCadastro[3].incluirEntrada(3)

    return subFrameCadastro

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
    
    interface = Interface(conjuntoProcCaches, memoriaPrincipal)
    interface.mainloop()
    