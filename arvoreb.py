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

    z.chaves = y.chaves[t+1:]

    if not y.folha:
        for j in range(0, t):
            z.filhos.append(y.filhos[j + t + 1])

    x.filhos.insert(i + 1, z)
    x.chaves.insert(i, y.chaves[t])

    y.chaves = y.chaves[0:t]


def insere_no_nodo(x: Nodo, c, t:int):
    i = len(x.chaves) - 1

    if x.folha:
        bisect.insort(x.chaves, c)
    else:
        while i >= 0 and c < x.chaves[i]:
            i = i - 1
        y = x.filhos[i + 1]
        overflow = insere_no_nodo(y, c, t)
        if overflow:
            particiona_filhos_arvore_b(x, i + 1, t)

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
