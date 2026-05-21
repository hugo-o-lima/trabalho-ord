from constantes import *
import os
from typing import List

class Interpretador:
    def __init__(self, caminho_operacoes: str = "arquivo_operacoes"):
        self.caminho_operacoes = caminho_operacoes
        
        self.indice_primario: List[list] = []
        self.indice_genero: List[list] = []
        self.indice_publicadora: List[list] = []
        self.lista_invertida: List[list] = []

    def carregar_todos_os_indices(self):
        self.__carregar_lista_invertida()
        self.__carregar_indice_primario()
        self.indice_genero = self.__carregar_indice_secundario(CAMINHO_INDICE_GENEROS)
        self.indice_publicadora = self.__carregar_indice_secundario(CAMINHO_INDICE_PUBLICADORAS)

    def salvar_todos_os_indices(self):
        self.__salvar_indice(CAMINHO_INDICE_PRIMARIO, self.indice_primario)
        self.__salvar_indice(CAMINHO_INDICE_GENEROS, self.indice_genero)
        self.__salvar_indice(CAMINHO_INDICE_PUBLICADORAS, self.indice_publicadora)
        self.__salvar_indice(CAMINHO_LISTA_INVERTIDA, self.lista_invertida)
    
    def interpretar_operacoes(self):
        lst_operacoes = self.__ler_operacoes()
        lst_id_operacoes = []
        for linha in lst_operacoes:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split(" ", 1)
            codigo = partes[0]
            argumento = partes[1] if len(partes) > 1 else ""
            encontrado = False
            for op in range(len(LISTA_OPERACOES)):
                if codigo == LISTA_OPERACOES[op]:
                    lst_id_operacoes.append([op, argumento])
                    encontrado = True
                    break
            if not encontrado:
                print(f"Erro: operação '{codigo}' não encontrada.")
                return []
        return lst_id_operacoes

    def __salvar_indice(self, caminho, dados):
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            for entrada in dados:
                arquivo.write(f"{entrada[0]}|{entrada[1]}\n")

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

    def __carregar_indice_primario(self):
        if not os.path.exists(CAMINHO_INDICE_PRIMARIO):
            print("Erro: Arquivo de índice primário não encontrado.")
            return

        with open(CAMINHO_INDICE_PRIMARIO, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue

                id_jogo, offset = linha.split("|")
                self.indice_primario.append([id_jogo, int(offset)])

    def __ler_operacoes(self):
        if not os.path.exists(self.caminho_operacoes):
            raise FileNotFoundError(f"Não foi encontrado arquivo {self.caminho_operacoes}.")
        
        arquivo = open(self.caminho_operacoes, 'r')
        str_operacoes = arquivo.read()
        arquivo.close()

        lst_operacoes = str_operacoes.split("\n")

        return lst_operacoes