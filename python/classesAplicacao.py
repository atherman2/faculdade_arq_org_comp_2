class DadosProduto:

    def __init__(self):
        
        self.valorCompra = 0
        self.valorVenda = 0
        self.quantidadeEmEstoque = 0
        self.mercadoEmQueEstá = 0

class GerenciaProdutos:

    def __init__(self):
        
        self.dicionarioProdutosIndices: dict[(str, int)] = {}
        self.listaEspacosDisponiveis = [-1]
        self.ultimoIndiceDeProduto = -1
        self.maximoProdutos = 0
    
    def estaSemEspacosDisponiveisInternos(self):

        return self.listaEspacosDisponiveis[-1] == -1
    
    def chegouNoIndiceMaximo(self):

        return (self.maximoProdutos - 1) <= self.ultimoIndiceDeProduto

    def adicionaProduto(self, nomeProduto):
        
        if self.dicionarioProdutosIndices.get(nomeProduto) != None:

            return -1
        
        elif self.chegouNoIndiceMaximo() and self.estaSemEspacosDisponiveisInternos():

            return -2
        
        elif not self.estaSemEspacosDisponiveisInternos():

            indiceProduto = self.listaEspacosDisponiveis.pop()
            self.dicionarioProdutosIndices[nomeProduto] = indiceProduto
            return indiceProduto
        
        else:

            self.ultimoIndiceDeProduto += 1
            self.dicionarioProdutosIndices[nomeProduto] = self.ultimoIndiceDeProduto
            return self.ultimoIndiceDeProduto
    
    def removeProduto(self, nomeProduto):

        if self.dicionarioProdutosIndices.get(nomeProduto) ==  None:

            return -1
        
        else:

            indiceProduto = self.dicionarioProdutosIndices.pop(nomeProduto)
            self.listaEspacosDisponiveis.append(indiceProduto)
            return indiceProduto
    
    def consultaProduto(self, nomeProduto):

        return self.dicionarioProdutosIndices.get(nomeProduto)

if __name__ == "__main__":

    gerenciaProdutos = GerenciaProdutos()
    print(gerenciaProdutos.adicionaProduto("Banana"))
    gerenciaProdutos.maximoProdutos = 16

    indiceBanana = gerenciaProdutos.adicionaProduto("Banana")
    print(indiceBanana)
    indiceLimao = gerenciaProdutos.adicionaProduto("Limão")
    print(indiceLimao)
    
    print(gerenciaProdutos.consultaProduto("Banana"))
    print(gerenciaProdutos.consultaProduto("Limão"))

    indiceBanana = gerenciaProdutos.adicionaProduto("Banana")
    print(indiceBanana)
    
    indiceRoma = gerenciaProdutos.adicionaProduto("Romã")
    print(indiceRoma)
    
    indiceLimao = gerenciaProdutos.removeProduto("Limão")
    print(indiceLimao)
    indiceMelancia = gerenciaProdutos.removeProduto("Melancia")
    print(indiceMelancia)
    
    indiceLimao = gerenciaProdutos.adicionaProduto("Limão")
    print(indiceLimao)