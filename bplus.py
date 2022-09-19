
from multiprocessing.sharedctypes import Value
from typing import List

class Nodo:
    def __init__(self):
        self.chaves: List[any] = []
        self.valores: List[any] = []
        self.filhos: List[Nodo] = []
        self.esq: Nodo | None = None
        self.dir: Nodo | None = None
        self.folha: bool = False

    def insere(self, chave, valor, ordem) -> bool:
        # Encontra posição de inserção
        i = 0
        while (i < len(self.chaves)) and (chave > self.chaves[i]):
            i = i + 1 

        if self.folha:
            # se i < len(self.chaves), em vez de estourar erro, simplesmente apende à lista, o que é bom
            self.chaves.insert(i, chave)
            self.valores.insert(i, valor)
        else:
            filho = self.filhos[i]
            overflow = filho.insere(chave, valor, ordem)
            if overflow:
                self.particiona(i, ordem)

        return len(self.chaves) > 2*ordem

    def particiona(self, indiceParticao, ordem):
        nodoPai = self
        nodoMenor = nodoPai.filhos[indiceParticao]

        # teste de sanidade
        if len(nodoMenor.chaves) != (2*ordem + 1):
            raise ValueError('Nodo não está em estado de overflow')

        # cria nodo da partição
        nodoMaior = Nodo()
        nodoMaior.folha = nodoMenor.folha

        # liga os dois nodos
        if nodoMenor.folha:
            nodoMaior.esq = nodoMenor
            nodoMaior.dir = nodoMenor.dir
            if nodoMaior.dir:
                nodoMaior.dir.esq = nodoMaior
            nodoMenor.dir = nodoMaior

        # insere o nodoMaior no nodo pai
        meio = nodoMenor.chaves[ordem]
        nodoPai.chaves.insert(indiceParticao, meio) 
        nodoPai.filhos.insert(indiceParticao+1, nodoMaior)

        # distribui as chaves
        chavesParaDividir = nodoMenor.chaves
        nodoMenor.chaves = chavesParaDividir[:ordem]
        
        if nodoMenor.folha:
            nodoMaior.chaves = chavesParaDividir[ordem:]
            # distribui os valores (apenas nodos folha tem)
            valsParaDividir = nodoMenor.valores
            nodoMenor.valores = valsParaDividir[:ordem]
            nodoMaior.valores = valsParaDividir[ordem:] # 
        else:
            nodoMaior.chaves = chavesParaDividir[ordem+1:] # pula a chave do meio
            # distribui os filhos (apenas nodos internos tem)
            filhosParaDividir = nodoMenor.filhos
            nodoMaior.filhos = filhosParaDividir[ordem+1:]
            nodoMenor.filhos = filhosParaDividir[:ordem+1]

    def remove(self, chave, ordem) -> bool:
        pai = None
        n = self
        # encontra nodo folha que conteria a chave
        while not n.folha:
            i = 0
            while i < len(n.chaves) and chave > n.chaves[i]:
                i = i + 1
            pai = n
            n = n.filhos[i]

        if chave not in n.chaves:
            return

        j = n.chaves.index(chave)
        if len(n.chaves) > ordem:
            del n.chaves[j]
            del n.valores[j]
            return

        if n.esq and len(n.esq.chaves) > ordem:
            del n.chaves[j]
            del n.valores[j]
            n.insere(pai.chaves[i], pai.valores[i])

            # maior da esquerda toma lugar da chave no pai
            k = len(n.esq.chaves) - 1
            pai.chaves[i] = n.esq.chaves[k]
            pai.valores[i] = n.esq.valores[k]
            
            del n.esq.chaves[k]
            del n.esq.valores[k]
        elif n.dir and len(n.dir.chaves) > ordem:
            del n.chaves[j]
            del n.valores[j]
            n.insere(pai.chaves[i], pai.valores[i])

            # menor da direita toma lugar da chave no pai
            k = 0
            pai.chaves[i] = n.dir.chaves[k]
            pai.valores[i] = n.dir.valores[k]

            del n.dir.chaves[k]
            del n.dir.valores[k]

        # nenhum vizinho tem espaço
        del n.chaves[j]
        del n.valores[j]

        if n.dir:
            # Fusão à direita
            n.chaves = n.chaves + [pai.chaves[i]] + n.dir.chaves
            n.valores = n.valores + [pai.valores[i]] + n.dir.valores
            
            n.dir = n.dir.dir
            n.dir.esq = n
            del pai.filhos[i+1]

            del pai.chaves[i]
            del pai.valores[i]
        elif n.esq:
            # Fusão à esquerda
            n.chaves = n.esq.chaves + [pai.chaves[i]] + n.chaves
            n.valores = n.valores + [pai.valores[i]] + n.valores

            n.esq = n.esq.esq
            n.esq.dir = n
            del pai.filhos[i-1]
            del pai.chaves[i]
            del pai.valores[i]

def move_registro(n1:Nodo, i, n2:Nodo, k):
    n1.chaves[i] = n2.chaves[k]
    n1.valores[i] = n2.valores[k]
    del n2.chaves[k]
    del n2.valores[k]

def nodos_fusao(esq:Nodo, dir:Nodo, pai:Nodo, i):
    esq.chaves = esq.chaves + [pai.chaves[i]] + dir.chaves
    esq.valores = esq.valores + [pai.valores[i]] + dir.valores
    esq.dir = esq.dir.dir
    esq.dir = esq
    del pai.filhos[i+1]
    del pai.chaves[i]
    del pai.valores[i]

def nodo_remove_simples(n: Nodo, pai: Nodo, i, chave, ordem):
    if n.folha and pai:
        if chave not in n.chaves:
            return

        j = n.chaves.index(chave)
        del n.chaves[j]
        del n.valores[j]

        if n.esq and len(n.esq.chaves) > ordem:
            n.insere(pai.chaves[i], pai.valores[i])
            # maior da esquerda toma lugar da chave no pai
            move_registro(pai, i, n.esq, len(n.esq.chaves) - 1)
        elif n.dir and len(n.dir.chaves) > ordem:
            n.insere(pai.chaves[i], pai.valores[i])
            # menor da direita toma lugar da chave no pai
            move_registro(pai, i, n.dir, 0)

        # nenhum vizinho tem espaço
        if n.dir:
            nodos_fusao(n, n.dir, pai, i)
        elif n.esq:
            # Fusão à esquerda
            nodos_fusao(n.esq, n, pai, i)
        
def busca_nodo(n:Nodo, chave):
    if n.folha:
        return n
    i = 0
    while i < len(n.chaves) and chave >= n.chaves[i]:
        i = i + 1
    return busca_nodo(n.filhos[i], chave)

def busca_valor(n:Nodo, chave):
    n = busca_nodo(n, chave)
    try:
        return n.valores[n.chaves.index(chave)]
    except ValueError:
        return None

class ArvoreB:
    def __init__(self, ordem:int = 3):
        self.raiz = Nodo()
        self.ordem = ordem
        self.raiz.folha = True
        self.tipoChave = None
        self.maiorChave = 0
        self.numValores = 0

    def insere(self, chave, valor):
        if self.tipoChave and type(chave) != self.tipoChave():
            raise ValueError(f'Tipo incorreto para chave, deve ser {self.tipoChave}')

        if isinstance(chave, int) and chave > self.maiorChave: self.maiorChave = chave

        overflow = self.raiz.insere(chave, valor, self.ordem)
        if overflow:
            s = Nodo()
            s.folha = False
            s.filhos.append(self.raiz)
            self.raiz = s
            s.particiona(0, self.ordem)

        self.numValores += 1

    def insere_valor(self, valor) -> int:
        """Insere um valor, gerando automaticamente chave inteira."""
        chave = self.maiorChave + 1
        self.insere(chave, valor)
        return chave

    def busca(self, chave):
        pass

    def iterar_sequencial(self):
        n = self.raiz
        while not n.folha:
            n = n.filhos[0]
        while n:
            for i in range(0, len(n.chaves)): yield (n.chaves[i], n.valores[i])
            n = n.dir

    def iterar_rev(self):
        n = self.raiz
        while not n.folha:
            n = n.filhos[-1]
        while n:
            # de n.chaves - 1 até 0
            for i in range(len(n.chaves) - 1, -1, -1): yield (n.chaves[i], n.valores[i])
            n = n.esq
 
    def __len__(self): return self.numValores
