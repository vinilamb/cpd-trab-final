import bplus as btree
import graphviz

arvore = btree.ArvoreB(2)

def nodeStr(node): return ";".join(map(str, node.chaves))

def gera_grafo_arvore():
    dot = graphviz.Graph()
    
    def nodeText(nodo: btree.Nodo):
        return ";".join(str(r) for r in nodo.chaves)

    ordem = 1
    def addNode(node, nomePai=None):
        nonlocal ordem
        nome = f'n{ordem}'
        dot.node(nome, label=nodeText(node), )
        if nomePai:
            dot.edge(nomePai, nome)
        if not node.folha:
            for filho in node.filhos:
                ordem = ordem + 1
                addNode(filho, nome)

    addNode(arvore.raiz, 0)

    dot.render(outfile='grafo.png', cleanup=True)

# while True:
#     try:
#         inputStr = input("Digite um número e um valor (opcional) para inserir na árvore B: ")
#     except KeyboardInterrupt: break

#     tokens = inputStr.split()
#     chave = tokens[0]
#     if len(tokens) > 1:
#         valor = tokens[1]
#     else:
#         valor = None

#     chave = int(chave)

#     arvore.insere(chave, valor)
#     print('inseridos ' + str((chave, valor)))

#     gera_grafo_arvore()

for i in range(0, 100): arvore.insere(i, None)

gera_grafo_arvore()
# arvore.insere(1, 'João')
# arvore.insere(20, 'Maria')
# arvore.insere(30, 'José')
# arvore.insere(btree.Registro(40, 'Pedro')
# arvore.insere(btree.Registro(550, 'Marcos'))
# arvore.insere(btree.Registro(600, 'André'))
# arvore.insere(btree.Registro(700, 'Roberto'))
# arvore.insere(btree.Registro(888, 'Antônio'))
# arvore.insere(btree.Registro(9000, 'Miguel'))
# arvore.insere(btree.Registro(2, 'Maicon'))
# arvore.insere(btree.Registro(44, 'Robinson'))

# btree.traverse_asc(arvore.raiz)