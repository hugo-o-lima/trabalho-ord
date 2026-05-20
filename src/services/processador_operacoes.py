import os
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

    def remover_registro(self, id_remocao, interpretador):

        pos_primario = self.busca_binaria(interpretador.indice_primario, id_remocao)
        
        if pos_primario == -1:
            # Padrão de saída exigido na especificação (EspecificacaoTrab1.pdf)
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

        self.__atualizar_lista_invertida(
            id_remocao, genero, interpretador.indice_genero, interpretador.lista_invertida
        )
        self.__atualizar_lista_invertida(
            id_remocao, publicadora, interpretador.indice_publicadora, interpretador.lista_invertida
        )

        print(f'Remoção do registro de chave "{id_remocao}"')
        return True

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