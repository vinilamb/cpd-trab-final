import bplus as arvoreb
import pandas as pd
from collections import OrderedDict
import pickle
import sys

# Aumenta o limite de recursão para permitir serializar a árvore com ordem baixa
sys.setrecursionlimit(10000)

ARQ_DAT = 'JOGOS.DAT'
ARQ_AK = 'jogos_play2_A-K.csv'
ARQ_LZ = 'jogos_play2_L-Z.csv'

ORDEM = 2
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

            elif inputStr.startswith('b'):
                chave = int(inputStr[1:].strip())
                valor = arvoreb.busca_valor(ARVORE.raiz, chave)
                if valor:
                    print(f'Encontrado: {valor}')
                else:
                    print("Sem valor com chave " + str(chave))

            elif inputStr.startswith('titulo'):
                termoBusca = inputStr[7:].strip().lower()
                if termoBusca in INDICE_POR_TITULO:
                    print(f'Encontrados {len(INDICE_POR_TITULO[termoBusca])} registros.')
                    for chave in INDICE_POR_TITULO[termoBusca]:
                        valor = arvoreb.busca_valor(ARVORE.raiz, chave)
                        print(f'{chave}: {valor}')
                else:
                    print(f'Nenhum registro encontrado. Termo="{termoBusca}"')         

            elif inputStr.startswith('listar'):
                print('listando todos os valores')
                for chave, valor in ARVORE.iterar_sequencial():
                    print(f'{chave}: {valor}')
                
            elif inputStr.startswith('indexar'):
                print('indexando termos no dicionários')
                INDICE_POR_TITULO = indexar()
                print(f'obtidos {len(INDICE_POR_TITULO)} termos')

            elif inputStr.startswith('dicionario'):
                for k, postings in INDICE_POR_TITULO.items():
                    print(f'{k}: {len(postings)} -> {postings}')

            elif inputStr.startswith('persistir'):
                print(f'gravando em "{ARQ_DAT}"')
                with open(ARQ_DAT, 'wb') as f:
                    pickle.dump(ARVORE, f)

            elif inputStr.startswith('restaurar'):
                print(f'restaurando de "{ARQ_DAT}"')
                with open(ARQ_DAT, 'rb') as f:
                    ARVORE = pickle.load(f)

            elif inputStr.startswith('ordem'):
                try:
                    ordem = int(inputStr[5:])
                    if ordem == ORDEM:
                        print(f'ordem já é {ORDEM}')
                    novaArvore = arvoreb.ArvoreB(ordem)
                    for chave, valor in ARVORE.iterar_sequencial():
                        novaArvore.insere(chave, valor)
                    print(f'ordem alterada {ORDEM} -> {ordem}')
                    ORDEM = ordem
                    ARVORE = novaArvore
                except ValueError:
                    print('informe a ordem como um número')
            
            else:
                print('Comando desconhecido.')
        except KeyboardInterrupt:
            print("Encerrando o programa.")
            break