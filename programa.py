from operator import index
from typing import List
import arvoreb
import pandas as pd

ORDEM = 4
ARVORE = arvoreb.ArvoreB(ORDEM)
INDICE_POR_TITULO = {}

def carrega_dados_arquivo_original():
    global INDICE_POR_TITULO

    df = pd.read_csv('jogos_play2.csv')
    print(f'carregando {len(df)} registro(s)')

    registros = []
    for ix, row in df.iterrows():
        r = arvoreb.Registro(ix, row[0])
        ARVORE.insere(r)
        registros.append(r)

    INDICE_POR_TITULO = indexar(registros)
    
    print(INDICE_POR_TITULO.keys())
    print('terminou de carregar')

table = {ord(ch): ord(' ') for ch in list(r'/\?&%$#@!()|:,;[]-_•#.+')}
def tokenizar(string: str):
    global table
    string = string.lower()
    string = string.translate(table)
    return string.split()

def indexar(listaRegistros: List[arvoreb.Registro]):
    dictInvertido = {}
    for r in listaRegistros:
        tkns = tokenizar(r.valor)
        for t in tkns:
            if t in dictInvertido:
                dictInvertido[t].append(r.chave)
            else:
                dictInvertido[t] = [r.chave]
    return dictInvertido

if __name__ == '__main__':
    print('Trabalho Final de CPD - 2022/2')
    print('Por Vinicius Lamb Magalhães e Gabriel Zanini')
    print('Banco de dados de jogos de PlayStation 2')

    while True:
        try:
            inputStr = input("?: ").strip()

            if inputStr == 'carregar':
                ARVORE = arvoreb.ArvoreB(ORDEM)
                carrega_dados_arquivo_original()

            if inputStr.startswith('b'):
                chave = int(inputStr[1:].strip())
                valor = arvoreb.busca_valor_por_chave(ARVORE.raiz, chave)
                if valor:
                    print(f'Encontrado: {valor.valor}')
                else:
                    print("Sem valor com chave " + str(chave))

            if inputStr.startswith('titulo'):
                termoBusca = inputStr[7:].strip().lower()
                if termoBusca in INDICE_POR_TITULO:
                    print(f'Encontrados registros: {INDICE_POR_TITULO[termoBusca]}')
                    for chave in INDICE_POR_TITULO[termoBusca]:
                        valor = arvoreb.busca_valor_por_chave(ARVORE.raiz, chave)
                        print(valor)
                else:
                    print(f'Nenhum registro encontrado. Termo="{termoBusca}"')         

            if inputStr.startswith('list'):
                arvoreb.traverse_asc(ARVORE.raiz)
        except KeyboardInterrupt:
            print("Encerrando o programa.")
            break