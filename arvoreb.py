import bisect

def busca_nodo(nodo: 'Nodo', chave):
    indiceChave = 0

    while indiceChave < len(nodo.chaves) and chave > nodo.chaves[indiceChave]:
        indiceChave = indiceChave + 1
    
    if indiceChave < len(nodo.chaves) and chave == nodo.chave[indiceChave]:
        return nodo

    if nodo.folha:
        return None

    if indiceChave < len(nodo.chaves):
        nodo = nodo.filhos[indiceChave]
    else:
        nodo = nodo.filhos[indiceChave + 1]
    
    return busca_nodo(nodo, chave)

# No tem 2t + 1 chaves
def particiona_filhos_arvore_b(pai: 'Nodo', indice: int, ordem: int):
    z = Nodo()
    y:Nodo = pai.filhos[indice]
    z.folha = y.folha

    meio = y.chaves[ordem]
    esq = y.chaves[0:ordem]
    dir = y.chaves[ordem+1:]

    z.chaves = dir

    if not y.folha:
        z.filhos = y.filhos[ordem+1:]
        y.filhos = y.filhos[:ordem+1]
    
    pai.filhos.insert(indice + 1, z)
    pai.chaves.insert(indice, meio)

    y.chaves = esq

def insere_no_nodo(nodo: 'Nodo', chave, ordem:int):
    if nodo.folha:
        bisect.insort(nodo.chaves, chave)
    else:
        i = 0
        while i < len(nodo.chaves) and nodo.chaves[i] < chave:
            i = i + 1
            
        try:
            y = nodo.filhos[i]
        except IndexError as e:
            print(f'len filhos: {len(nodo.filhos)}, index: {i}') 
            print(f'chaves: {nodo.chaves}')
            raise e
        
        overflow = insere_no_nodo(y, chave, ordem)
        if overflow:
            particiona_filhos_arvore_b(nodo, i, ordem)

    return len(nodo.chaves) > 2*ordem

def insere_arvore(arvore: 'ArvoreB', chave):
    r = arvore.raiz
    
    overflow = insere_no_nodo(r, chave, arvore.ordem)

    if overflow:
        s = Nodo()
        arvore.raiz = s
        s.folha = False
        s.filhos.append(r)
        particiona_filhos_arvore_b(s, 0, arvore.ordem)

class Nodo:
    def __init__(self):
        self.filhos = []
        self.chaves = []
        self.folha = False

class ArvoreB:
    def __init__(self, ordem:int = 3):
        self.raiz = Nodo()
        self.ordem = ordem
        self.raiz.folha = True

    def insere(self, chave:int):
        insere_arvore(self, chave)