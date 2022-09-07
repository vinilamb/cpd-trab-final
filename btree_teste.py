import arvoreb as btree

arvore = btree.ArvoreB(1)

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

    imprime_arvore()