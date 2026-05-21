import os
from constantes import *

class Compactador:
    def __init__(self):
        pass

    def compactar_arquivo(self):
        lst_registros = self.__ler_validos()
        lst_offsets = self.__salvar_arquivo(lst_registros)
        return lst_offsets

    def __ler_validos(self):
        lst_registros_validos = []

        arq = open(CAMINHO_JOGOS, "rb")
        
        tamanho_bytes = arq.read(2)
        while tamanho_bytes:
            offset = arq.tell() - 2
            tamanho = int.from_bytes(tamanho_bytes, "little")
            conteudo = arq.read(tamanho).decode("utf-8")

            if not conteudo.startswith("*"):
                lst_registros_validos.append(conteudo)

            tamanho_bytes = arq.read(2)

        arq.close()
        return lst_registros_validos

    def __salvar_arquivo(self, lst_registros):
        if os.path.exists(CAMINHO_JOGOS):
            os.remove(CAMINHO_JOGOS)

        arq = open(CAMINHO_JOGOS, "wb")
        lst_offsets_novos = []

        for registro in lst_registros:
            offset_novo = arq.tell()
            lst_offsets_novos.append(offset_novo)
            
            conteudo_bytes = registro.encode('utf-8')
            tamanho = len(conteudo_bytes)
            tamanho_bytes = tamanho.to_bytes(2, byteorder='little')
            
            arq.write(tamanho_bytes)
            arq.write(conteudo_bytes)

        arq.close()
        return lst_offsets_novos