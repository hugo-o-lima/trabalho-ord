from constantes import *
import os

class Interpretador:
    def __init__(self, caminho_operacoes: str = "arquivo_operacoes"):
        self.caminho_operacoes = caminho_operacoes
        
        self.indice_genero = []
        self.indice_publicadora = []
        self.lista_invertida = []

    def carregar_todos_os_indices(self):
        self.__carregar_lista_invertida()
        
        self.indice_genero = self.__carregar_indice_secundario(CAMINHO_INDICE_GENEROS)
        self.indice_publicadora = self.__carregar_indice_secundario(CAMINHO_INDICE_PUBLICADORAS)

    def __carregar_lista_invertida(self):
        if not os.path.exists(CAMINHO_LISTA_INVERTIDA):
            print("Erro: Arquivo de lista invertida não encontrado.")
            return

        with open(CAMINHO_LISTA_INVERTIDA, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha: 
                    continue
                
                id_jogo, proximo_ponteiro = linha.split("|")
                self.lista_invertida.append([id_jogo, int(proximo_ponteiro)])

    def __carregar_indice_secundario(self, caminho_indice: str):
            if not os.path.exists(caminho_indice):
                return []

            indice_temporario = []
            with open(caminho_indice, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if not linha: continue
                    
                    chave_secundaria, pos_lista_invertida = linha.split("|")
                    indice_temporario.append([chave_secundaria, int(pos_lista_invertida)])
                    
            indice_temporario.sort() 
            return indice_temporario

    def __ler_operacoes(self):
        if not os.path.exists(self.caminho_operacoes):
            raise FileNotFoundError(f"Não foi encontrado arquivo {self.caminho_operacoes}.")
        
        arquivo = open(self.caminho_operacoes, 'r')
        str_operacoes = arquivo.read()
        arquivo.close()

        lst_operacoes = str_operacoes.split("\n")

        return lst_operacoes

    def interpretar_operacoes(self):
        # usa tipo ids pra identificar as operações pra não precisar iterar pelas strings toda vez q rodar uma operação (0=bp,1=bs1,etc.)
        # TODO: revisar se esse é o melhor jeito de fazer isso
        lst_operacoes = __ler_operacoes()
        lst_id_operacoes = []
        for i in lst_operacoes:
            for op in range(len(LISTA_OPERACOES)):
                if i == LISTA_OPERACOES[op]:
                    lst_id_operacoes.append(op)
                else:
                    print(f"Erro: operação {i} não encontrada.")
                    return