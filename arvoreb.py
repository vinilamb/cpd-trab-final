import bisect

class Nodo:
    def __init__(self):
        self.filhos = []
        self.chaves = []
        self.folha = False

    def insere(self, chave): pass

class ArvoreB:
    def __init__(self, ordem = 3):
        self.raiz = Nodo()
        self.ordem = ordem
        self.raiz.folha = True

    def insere(self, chave):
        self.raiz.insere(chave)

def busca_nodo(nodo: Nodo, chave):
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
def particiona_filhos_arvore_b(x: Nodo, i: int, t: int):
    z = Nodo()
    y:Nodo = x.filhos[i]
    z.folha = y.folha

    meio = y.chaves[t]
    esq = y.chaves[0:t]
    dir = y.chaves[t+1:]

    z.chaves = dir

    if not y.folha:
        z.filhos = y.filhos[t+1:]
        y.filhos = y.filhos[:t+1]
    
    x.filhos.insert(i + 1, z)
    x.chaves.insert(i, meio)

    y.chaves = esq


def insere_no_nodo(x: Nodo, c, t:int):
    if x.folha:
        bisect.insort(x.chaves, c)
    else:
        i = 0
        while i < len(x.chaves) and x.chaves[i] < c:
            i = i + 1
            
        try:
            y = x.filhos[i]
        except IndexError as e:
            print(f'len filhos: {len(x.filhos)}, index: {i}') 
            print(f'chaves: {x.chaves}')
            raise e
        
        overflow = insere_no_nodo(y, c, t)
        if overflow:
            particiona_filhos_arvore_b(x, i, t)

    return len(x.chaves) > 2*t

def insere_arvore(T: ArvoreB, c):
    r = T.raiz

    overflow = insere_no_nodo(r, c, T.ordem)

    if overflow:
        s = Nodo()
        T.raiz = s
        s.folha = False
        s.filhos.append(r)
        particiona_filhos_arvore_b(s, 0, T.ordem)
