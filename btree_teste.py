import arvoreb as btree
import graphviz

arvore = btree.ArvoreB(2)

def nodeStr(node): return ";".join(map(str, node.chaves))

def gera_grafo_arvore():
    dot = graphviz.Graph()
    
    def nodeText(nodo: btree.Nodo):
        print(nodo.registros)
        return ";".join(str(r.chave) for r in nodo.registros)

    ordem = 0
    def addNode(node, nomePai=None):
        nonlocal ordem
        nome = f'n{ordem}'
        dot.node(nome, label=nodeText(node))
        if nomePai:
            dot.edge(nomePai, nome)
        if not node.folha:
            for filho in node.filhos:
                ordem = ordem + 1
                addNode(filho, nome)

    addNode(arvore.raiz, 0)

    dot.render(outfile='grafo.png', cleanup=True)

while True:
    try:
        comStr = input("Digite um número para inserir na árvore B: ")
    except KeyboardInterrupt: break

    try:
        numero = int(comStr)
    except:
        print("NÚMERO!!!")
        continue
    
    reg = btree.Registro(numero, None)
    arvore.insere(reg)

    gera_grafo_arvore()