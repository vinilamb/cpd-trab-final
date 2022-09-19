import bplus as arvoreb
import pandas as pd
from collections import OrderedDict
import pickle
import sys

class Jogo():
    def __init__(self, titulo, dev, data):
        self.titulo = titulo
        self.dev = dev
        self.data = data
    def __str__(self):
        return f'"{self.titulo}", por {self.dev}, lançado em {self.data}'

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
        titulo = row[0]
        dev = row[1]
        data = row[2]
        jogo = Jogo(titulo, dev, data)
        ARVORE.insere_valor(jogo)

table = {ord(ch): ord(' ') for ch in list(r'/\?&%$#@!()|:,;[]-_•#.+')}
def tokenizar(string: str):
    string = string.lower()
    string = string.translate(table)
    return string.split()

def indexar():
    dictInvertido = OrderedDict()
    for chave, valor in ARVORE.iterar_sequencial():
        tkns = tokenizar(valor.titulo)
        for t in tkns:
            if t in dictInvertido:
                dictInvertido[t].append(chave)
            else:
                dictInvertido[t] = [chave]
    return dictInvertido

### Implementação dos comandos
def cmd_carregar():
    global ARVORE
    ARVORE = arvoreb.ArvoreB(ORDEM)
    carrega_arquivo(ARQ_AK)
    carrega_arquivo(ARQ_LZ)

def cmd_busca(argLine: str):
    try:
        chave = int(argLine)
        valor = arvoreb.busca_valor(ARVORE.raiz, chave)
    except:
        print('ERRO: Chave primária não informada.')

    if valor:
        print(f'Encontrado: {valor}')
    else:
        print("Sem valor com chave " + str(chave))

def cmd_titulo(argLine):
    if not argLine:
        print('ERRO: Informe um termo para busca.')
        return
    
    if len(INDICE_POR_TITULO) == 0:
        print('O dicionário está vazio. Tenha certeza de executar o comando "indexar" antes de tentar fazer uma busca.')

    termoBusca = argLine.strip().lower()
    if termoBusca in INDICE_POR_TITULO:
        print(f'Encontrados {len(INDICE_POR_TITULO[termoBusca])} registros.')
        for chave in INDICE_POR_TITULO[termoBusca]:
            valor = arvoreb.busca_valor(ARVORE.raiz, chave)
            print(f'{chave}: {valor}')
    else:
        print(f'Nenhum registro encontrado. Termo="{termoBusca}"')         

def cmd_listar():
    print('listando todos os valores')
    for chave, valor in ARVORE.iterar_sequencial():
        print(f'{chave}: {valor}')

def cmd_indexar():
    global INDICE_POR_TITULO
    if len(ARVORE) == 0:
        print('A árvore está vazia, certifique-se de rodar o comando "carregar" antes de tentar gerar o índice.')
        return

    print('indexando termos no dicionários')
    INDICE_POR_TITULO = indexar()
    print(f'obtidos {len(INDICE_POR_TITULO)} termos')

def cmd_dicionario():
    for k, postings in INDICE_POR_TITULO.items():
        print(f'{k}: {len(postings)} -> {postings}')

def cmd_persistir():
    print(f'gravando em "{ARQ_DAT}"')
    with open(ARQ_DAT, 'wb') as f:
        pickle.dump(ARVORE, f)

def cmd_restaurar():
    print(f'restaurando de "{ARQ_DAT}"')
    with open(ARQ_DAT, 'rb') as f:
        ARVORE = pickle.load(f)

def cmd_ordem(argLine):
    try:
        ordem = int(argLine)
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

def get_command(inputStr:str):
    inputStr = inputStr.strip()
    cmd = resto = None
    try:
        i = inputStr.index(' ')
        cmd = inputStr[:i]
        resto = inputStr[i:].lstrip()
    except ValueError:
        cmd = inputStr
    return (cmd, resto)

TEXTO_AJUDA = """Comandos implementados:
  carregar: carregar os arquivos de dados padrão
  busca: busca o registro com a chave informada
  titulo: busca os títulos por token
  indexar: gera o índice por título"""

if __name__ == '__main__':
    print('=' * 65)
    print('| Trabalho Final de CPD - 2022/2')
    print('| Banco de dados de jogos de PlayStation 2')
    print('|  - Por Vinicius Lamb Magalhães e Gabriel Zanini © 2022')
    print('=' * 65)
    
    # Loop principal
    while True:
        try:
            inputStr = input('?: ')
            comando, restoDaLinha = get_command(inputStr)

            if comando == 'carregar':
                cmd_carregar()
            elif comando == 'busca':
                cmd_busca(restoDaLinha)
            elif comando == 'titulo':
                cmd_titulo(restoDaLinha)
            elif comando == 'listar':
                cmd_listar()
            elif comando == 'indexar':
                cmd_indexar()
            elif comando == 'dicionario':
                cmd_dicionario()
            elif comando == 'persistir':
                cmd_persistir()
            elif comando == 'restaurar':
                cmd_restaurar()
            elif comando == 'ordem':
                cmd_ordem(restoDaLinha)
            elif comando == 'ajuda':
                print(TEXTO_AJUDA)
            else:
                print('Comando desconhecido. O comando "ajuda" lista os comandos implementados')
        
        except KeyboardInterrupt:
            print("Encerrando o programa.")
            break