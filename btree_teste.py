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
        inputStr = input("Digite um número e um valor para inserir na árvore B: ")
    except KeyboardInterrupt: break

    i_space = inputStr.find(' ')
    if i_space != -1:
        numOrCmd = inputStr[:i_space]
        resto = inputStr[i_space+1:]
        
        if numOrCmd == 'b':  
            # busca
            valor = btree.busca_nodo_2(arvore.raiz, int(resto))
            if valor:
                print(f'Encontrado: ' + valor.__repr__())
            else:
                print(f'chave {int(resto)} sem valor')

        elif numOrCmd == 'r':
            pass
        elif numOrCmd == 'i': 
            i_space = resto.find(' ')
            if i_space != -1:
                chave_str = resto[:i_space]
                valor = resto[i_space+1:].strip()
            else:
                chave_str = resto
                valor=None
            
            chave = int(chave_str)
            arvore.insere(btree.Registro(chave, valor))

            print('inseridos ' + str((chave, valor)))

    # reg = btree.Registro(numero, valor)
    # arvore.insere(reg)

    # gera_grafo_arvore()

# arvore.insere(btree.Registro(1, 'João'))
# arvore.insere(btree.Registro(2, 'Maria'))
# arvore.insere(btree.Registro(3, 'José'))
# arvore.insere(btree.Registro(4, 'Pedro'))
# arvore.insere(btree.Registro(5, 'Marcos'))
# arvore.insere(btree.Registro(6, 'André'))
# arvore.insere(btree.Registro(7, 'Roberto'))
# arvore.insere(btree.Registro(8, 'Antônio'))
# arvore.insere(btree.Registro(9, 'Miguel'))