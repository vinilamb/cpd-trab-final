from typing import List
import bplus as arvoreb
import pandas as pd
from collections import OrderedDict

ARQ_AK = 'jogos_play2_L-Z.csv'
ARQ_LZ = 'jogos_play2_A-K.csv'

ORDEM = 4
ARVORE = arvoreb.ArvoreB(ORDEM)
INDICE_POR_TITULO = OrderedDict()

def carrega_arquivo(arquivo):
    df = pd.read_csv(arquivo)
    print(f'carregando {len(df)} registro(s) de "{arquivo}"')
    for ix, row in df.iterrows():
        ARVORE.insere_valor(row[0])

table = {ord(ch): ord(' ') for ch in list(r'/\?&%$#@!()|:,;[]-_•#.+')}
def tokenizar(string: str):
    global table
    string = string.lower()
    string = string.translate(table)
    return string.split()

def indexar():
    dictInvertido = OrderedDict()
    for chave, valor in ARVORE.iterar_sequencial():
        tkns = tokenizar(valor)
        for t in tkns:
            if t in dictInvertido:
                dictInvertido[t].append(chave)
            else:
                dictInvertido[t] = [chave]
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
                carrega_arquivo(ARQ_AK)
                carrega_arquivo(ARQ_LZ)

            if inputStr.startswith('b'):
                chave = int(inputStr[1:].strip())
                valor = arvoreb.busca_valor(ARVORE.raiz, chave)
                if valor:
                    print(f'Encontrado: {valor}')
                else:
                    print("Sem valor com chave " + str(chave))

            if inputStr.startswith('titulo'):
                termoBusca = inputStr[7:].strip().lower()
                if termoBusca in INDICE_POR_TITULO:
                    print(f'Encontrados {len(INDICE_POR_TITULO[termoBusca])} registros.')
                    for chave in INDICE_POR_TITULO[termoBusca]:
                        valor = arvoreb.busca_valor(ARVORE.raiz, chave)
                        print(f'{chave}: {valor}')
                else:
                    print(f'Nenhum registro encontrado. Termo="{termoBusca}"')         

            if inputStr.startswith('listar'):
                print('listando todos os valores')
                for chave, valor in ARVORE.iterar_sequencial():
                    print(f'{chave}: {valor}')
                
            if inputStr.startswith('indexar'):
                print('indexando termos no dicionários')
                INDICE_POR_TITULO = indexar()
                print(f'obtidos {len(INDICE_POR_TITULO)} termos')

            if inputStr.startswith('dicionario'):
                for k, postings in INDICE_POR_TITULO.items():
                    print(f'{k}: {len(postings)} -> {postings}')

        except KeyboardInterrupt:
            print("Encerrando o programa.")
            break