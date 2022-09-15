import arvoreb
import pandas as pd

ORDEM = 4
ARVORE = arvoreb.ArvoreB(ORDEM)

def carrega_dados_arquivo_original():
    df = pd.read_csv('jogos_play2.csv')
    print(f'carregando {len(df)} registro(s)')
    for ix, row in df.iterrows():
        arvore.insere(arvoreb.Registro(ix, row[0]))
    print('terminou de carregar')

if __name__ == '__main__':
    print('Trabalho Final de CPD - 2022/2')
    print('Por Vinicius Lamb Magalhães e Gabriel Zanini')
    print('Banco de dados de jogos de PlayStation 2')

    while True:
        try:
            inputStr = input("?: ").strip()

            if inputStr == 'carregar':
                arvore = arvoreb.ArvoreB(ORDEM)
                carrega_dados_arquivo_original()

            if inputStr.startswith('b'):
                chave = int(inputStr[1:].strip())
                valor = arvoreb.busca_nodo_2(arvore.raiz, chave)
                if valor:
                    print(f'Encontrado: {valor.valor}')
                else:
                    print("Sem valor com chave " + str(chave))

        except KeyboardInterrupt:
            print("Encerrando o programa.")
            break