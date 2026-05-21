import os
import math
from constantes import *

class ProcessadorOperacoes:
    def __init__(self):
        pass

    def busca_binaria(self, lst_indices, chave_buscada):
        left = 0
        right = len(lst_indices) - 1
        
        while left <= right:
            meio = (left + right) // 2
            chave_meio = lst_indices[meio][0]
            
            if chave_meio == chave_buscada:
                return meio
            elif chave_meio > chave_buscada:
                right = meio - 1
            else:
                left = meio + 1
                
        return -1

    def busca_primaria(self, id_buscado, interpretador):
        print(f'Busca pelo registro de ID "{id_buscado}"')
        pos = self.busca_binaria(interpretador.indice_primario, id_buscado)
        
        if pos == -1:
            print("Registro não encontrado!")
            return

        offset = int(interpretador.indice_primario[pos][1])
        self.__imprimir_registro(offset)

    def busca_secundaria(self, chave_buscada, indice_secundario, prefixo_mensagem, interpretador):
        pos_sec = self.busca_binaria(indice_secundario, chave_buscada)
        
        if pos_sec == -1:
            print(f'Busca por registros {prefixo_mensagem} "{chave_buscada}" (0 registros)')
            return

        ids_encontrados = []
        pos_atual = int(indice_secundario[pos_sec][1])

        while pos_atual != -1:
            ids_encontrados.append(interpretador.lista_invertida[pos_atual][0])
            pos_atual = int(interpretador.lista_invertida[pos_atual][1])

        print(f'Busca por registros {prefixo_mensagem} "{chave_buscada}" ({len(ids_encontrados)} registros)')
        
        for id_jogo in ids_encontrados:
            pos_prim = self.busca_binaria(interpretador.indice_primario, id_jogo)
            if pos_prim != -1:
                offset = int(interpretador.indice_primario[pos_prim][1])
                self.__imprimir_registro(offset)

    def inserir_registro(self, novo_registro, interpretador):
        campos = novo_registro.split("|")
        id_novo = campos[0]
        genero = campos[3]
        publicadora = campos[4]

        if self.busca_binaria(interpretador.indice_primario, id_novo) != -1:
            print(f"Mensagem de erro: ID {id_novo} duplicado. Registro descartado.")
            return False

        conteudo_bytes = novo_registro.encode("utf-8")
        tamanho = len(conteudo_bytes)
        tamanho_bytes = tamanho.to_bytes(2, "little")

        with open(CAMINHO_JOGOS, "r+b") as arq:
            arq.seek(0, 2)
            offset = arq.tell()
            arq.write(tamanho_bytes)
            arq.write(conteudo_bytes)

        interpretador.indice_primario.append([id_novo, offset])
        interpretador.indice_primario.sort(key=lambda x: x[0])

        self.__inserir_na_lista_invertida(id_novo, genero, interpretador.indice_genero, interpretador.lista_invertida)
        self.__inserir_na_lista_invertida(id_novo, publicadora, interpretador.indice_publicadora, interpretador.lista_invertida)

        print(f'Inserção do registro de chave "{id_novo}" ({tamanho} bytes)')
        return True

    def remover_registro(self, id_remocao, interpretador):
        pos_primario = self.busca_binaria(interpretador.indice_primario, id_remocao)
        
        if pos_primario == -1:
            print(f'Remoção do registro de chave "{id_remocao}"')
            print("Registro não encontrado!")
            return False

        offset = int(interpretador.indice_primario[pos_primario][1])

        with open(CAMINHO_JOGOS, "r+b") as arq:
            arq.seek(offset)
            tamanho_bytes = arq.read(2)
            tamanho = int.from_bytes(tamanho_bytes, "little")
            
            conteudo_original = arq.read(tamanho).decode("utf-8")
            campos = conteudo_original.split("|")
            genero = campos[3]
            publicadora = campos[4]

            arq.seek(offset + 2)
            arq.write(b'*')

        interpretador.indice_primario.pop(pos_primario)

        self.__atualizar_lista_invertida(id_remocao, genero, interpretador.indice_genero, interpretador.lista_invertida)
        self.__atualizar_lista_invertida(id_remocao, publicadora, interpretador.indice_publicadora, interpretador.lista_invertida)

        print(f'Remoção do registro de chave "{id_remocao}" (offset = {offset})')
        return True

    def __imprimir_registro(self, offset):
        with open(CAMINHO_JOGOS, "rb") as arq:
            arq.seek(offset)
            tamanho_bytes = arq.read(2)
            if not tamanho_bytes:
                return
            tamanho = int.from_bytes(tamanho_bytes, "little")
            conteudo = arq.read(tamanho).decode("utf-8")
            
            if not conteudo.startswith("*"):
                print(conteudo)

    def __inserir_na_lista_invertida(self, id_novo, chave_secundaria, indice_secundario, lista_invertida):
        pos_sec = self.busca_binaria(indice_secundario, chave_secundaria)
        nova_pos_lista = len(lista_invertida)
        
        lista_invertida.append([id_novo, -1])

        if pos_sec == -1:
            indice_secundario.append([chave_secundaria, nova_pos_lista])
            indice_secundario.sort(key=lambda x: x[0])
        else:
            pos_atual = int(indice_secundario[pos_sec][1])
            pos_anterior = -1
            
            while pos_atual != -1:
                pos_anterior = pos_atual
                pos_atual = int(lista_invertida[pos_atual][1])
            
            if pos_anterior != -1:
                lista_invertida[pos_anterior][1] = nova_pos_lista

    def __atualizar_lista_invertida(self, id_remocao, chave_secundaria, indice_secundario, lista_invertida):
        pos_sec = self.busca_binaria(indice_secundario, chave_secundaria)
        if pos_sec == -1:
            return

        pos_atual = int(indice_secundario[pos_sec][1])
        pos_anterior = -1

        while pos_atual != -1:
            id_atual = lista_invertida[pos_atual][0]
            prox_pos = int(lista_invertida[pos_atual][1])

            if id_atual == id_remocao:
                if pos_anterior == -1:
                    if prox_pos == -1:
                        indice_secundario.pop(pos_sec)
                    else:
                        indice_secundario[pos_sec][1] = prox_pos
                else:
                    lista_invertida[pos_anterior][1] = prox_pos
                
                lista_invertida[pos_atual][0] = "-1"
                lista_invertida[pos_atual][1] = -1
                break

            pos_anterior = pos_atual
            pos_atual = prox_pos