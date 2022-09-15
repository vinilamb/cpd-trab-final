import bisect
from typing import NamedTuple

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

def busca_valor_por_chave(nodo: 'Nodo', chave):
    i = 0
    while i < len(nodo.registros) and nodo.registros[i].chave < chave:
        i = i + 1
    
    if i < len(nodo.registros) and nodo.registros[i].chave == chave:
        return nodo.registros[i]

    if not nodo.folha:
        return busca_valor_por_chave(nodo.filhos[i], chave)
    else:
        return None

# No tem 2t + 1 chaves
def particiona_filhos_arvore_b(pai: 'Nodo', indice: int, ordem: int):
    nodoMaior = Nodo()
    nodoMenor:Nodo = pai.filhos[indice]
    nodoMaior.folha = nodoMenor.folha

    meio = nodoMenor.registros[ordem]
    esq = nodoMenor.registros[0:ordem]
    dir = nodoMenor.registros[ordem+1:]

    nodoMaior.registros = dir

    if not nodoMenor.folha:
        nodoMaior.filhos = nodoMenor.filhos[ordem+1:]
        nodoMenor.filhos = nodoMenor.filhos[:ordem+1]
    
    pai.filhos.insert(indice + 1, nodoMaior)
    pai.registros.insert(indice, meio)

    nodoMenor.registros = esq

def insere_no_nodo(nodo: 'Nodo', registro: 'Registro', ordem:int):
    chave = registro.chave
    
    if nodo.folha:
        bisect.insort(nodo.registros, registro, key=lambda r: r.chave)
    else:
        i = 0
        while i < len(nodo.registros) and nodo.registros[i].chave < chave:
            i = i + 1
            
        y = nodo.filhos[i]
        
        overflow = insere_no_nodo(y, registro, ordem)
        if overflow:
            particiona_filhos_arvore_b(nodo, i, ordem)

    return len(nodo.registros) > 2*ordem

def insere_arvore(arvore: 'ArvoreB', registro: 'Registro'):
    r = arvore.raiz
    
    overflow = insere_no_nodo(r, registro, arvore.ordem)

    if overflow:
        s = Nodo()
        arvore.raiz = s
        s.folha = False
        s.filhos.append(r)
        particiona_filhos_arvore_b(s, 0, arvore.ordem)

def traverse_asc(nodo: 'Nodo'):
    if nodo.folha:
        for r in nodo.registros:
            print(r)
        return
    
    for i, n in enumerate(nodo.filhos):
        traverse_asc(n)
        if i < len(nodo.registros):
            print(nodo.registros[i])

class Registro(NamedTuple):
    chave:any
    valor:any

class Nodo:
    def __init__(self):
        self.registros = []
        self.filhos = []
        self.folha = False

class ArvoreB:
    def __init__(self, ordem:int = 3):
        self.raiz = Nodo()
        self.ordem = ordem
        self.raiz.folha = True

    def insere(self, registro: Registro):
        insere_arvore(self, registro)

    def busca(self, chave):
        return busca_valor_por_chave(self.raiz, chave)