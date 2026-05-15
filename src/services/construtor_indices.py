import os

class ConstrutorIndices:
    def __init__(self) -> None:
        self.id = 0
        self.nome = 1
        self.ano = 2
        self.genero = 3
        self.publicadora = 4

    def construir_indices(self, lst_jogos: list[list[str]]):
        indice_primario = []
        
        for i in range(len(lst_jogos)):
            id_jogo = lst_jogos[i][self.id]
            indice_primario.append([id_jogo, str(i)])
        
        indice_primario.sort(key=lambda x: int(x[0]))

        self.__salvar_ind("primario.ind", indice_primario)

        idx_gen, lst_gen = self.__gerar_lst_invertida(lst_jogos, self.genero)
        idx_pub, lst_pub = self.__gerar_lst_invertida(lst_jogos, self.publicadora)
        
        return idx_gen, lst_gen, idx_pub, lst_pub

    def __salvar_ind(self, nome_arq: str, dados):
        if os.path.exists(nome_arq):
            os.remove(nome_arq)

        arquivo = open(nome_arq, 'w')
        
        for i in dados:
            arquivo.write(f"{i[0], i[1]}\n")
        
        arquivo.close()

    def __gerar_lst_invertida(self, lst_jogos: list[list[str]], idx_col: int):
        agrupados = []

        for jogo in lst_jogos:
            chave = jogo[idx_col]
            id = jogo[self.id]

            item = ""
            index = 0
            while item != "" or index == (len(lst_jogos) - 1):
                if chave == lst_jogos[index]:
                    item = lst_jogos[index][self.id]
                else:
                    index += 1
                    agrupados.append([chave, id])
            
            agrupados.sort()

        indice_secundario = []
        lista_invertida_local = []
        posicao_atual_lst = 0

        for grupo in agrupados:
            chave = grupo[0]
            ids = grupo[1:]
            
            indice_secundario.append([chave, str(posicao_atual_lst)])
            
            for i in range(len(ids)):
                proximo = str(posicao_atual_lst + 1) if i < len(ids) - 1 else "-1"
                lista_invertida_local.append([ids[i], proximo])
                posicao_atual_lst += 1

        return indice_secundario, lista_invertida_local