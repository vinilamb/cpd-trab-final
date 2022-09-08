import arvoreb as btree
import graphviz

arvore = btree.ArvoreB(2)

def imprime_arvore():
    nivel = 1
    nodos = [arvore.raiz] 
    while True:
        linha = f'{nivel}: ' + " | ".join([('F' if n.folha else 'I' ) + ':' + str(n.chaves) for n in nodos])
        print(linha)

        if nodos[0].folha:
            break
        
        listaFilhos = [] 
        for nodos in [x.filhos for x in nodos]:
            listaFilhos = listaFilhos + nodos
        
        nodos = listaFilhos
        nivel = nivel + 1

def nodeStr(node): return ";".join(map(str, node.chaves))

def gera_grafo_arvore():
    dot = graphviz.Graph()
    
    ordem = 0
    def addNode(node, nomePai=None):
        nonlocal ordem
        nome = f'n{ordem}'
        dot.node(nome, label=";".join(map(str, node.chaves)))
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
    
    btree.insere_arvore(arvore, int(comStr))

    gera_grafo_arvore()