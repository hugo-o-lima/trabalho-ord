import os

class ConstrutorIndices:
    def __init__(self) -> None:
        self.id = 0
        self.nome = 1
        self.ano = 2
        self.genero = 3
        self.publicadora = 4
        self.plataforma = 5

    def construir_indices(self, caminho: str = "games.dat"):
        lst_jogos = self.__ler_games_dat(caminho)

        indice_primario = []
        for campos, offset in lst_jogos:
            indice_primario.append([campos[self.id], str(offset)])
            
        indice_primario.sort()
        self.__salvar_ind("primario.ind", indice_primario)

        idx_gen, lst_gen = self.__gerar_lst_invertida(lst_jogos, self.genero, 0)
        idx_pub, lst_pub = self.__gerar_lst_invertida(
            lst_jogos, self.publicadora, len(lst_gen)
        )

        self.__salvar_ind("genero.ind", idx_gen)
        self.__salvar_ind("publicadora.ind", idx_pub)
        self.__salvar_ind("listaInvertida.lst", lst_gen + lst_pub)

        return indice_primario, idx_gen, lst_gen, idx_pub, lst_pub

    def __ler_games_dat(self, caminho: str = "games.dat"):
        lst_jogos = []
        arq = open(caminho, "rb")
        
        tamanho_bytes = arq.read(2)
        while tamanho_bytes:
            offset = arq.tell() - 2
            tamanho = int.from_bytes(tamanho_bytes, "little")
            conteudo = arq.read(tamanho).decode("utf-8")

            if not conteudo.startswith("*"):
                campos = conteudo.split("|")
                lst_jogos.append((campos, offset))

            tamanho_bytes = arq.read(2)

        arq.close()
        return lst_jogos

    def __salvar_ind(self, nome_arq: str, dados):
        if os.path.exists(nome_arq):
            os.remove(nome_arq)

        arquivo = open(nome_arq, "w", encoding="utf-8")
        for entrada in dados:
            arquivo.write(f"{entrada[0]}|{entrada[1]}\n")
        arquivo.close()

    def __gerar_lst_invertida(self, lst_jogos: list, idx_col: int, offset: int):
        grupos = {}
        for campos, _ in lst_jogos:
            chave = campos[idx_col]
            id_jogo = campos[self.id]
            if chave not in grupos:
                grupos[chave] = []
            grupos[chave].append(id_jogo)

        chaves_ordenadas = sorted(grupos.keys())

        indice_secundario = []
        lista_invertida = []
        posicao_atual = offset

        for chave in chaves_ordenadas:
            ids = grupos[chave]

            indice_secundario.append([chave, str(posicao_atual)])

            for i in range(len(ids)):
                if i < len(ids) - 1:
                    proximo = str(posicao_atual + 1)
                else:
                    proximo = "-1"
                lista_invertida.append([ids[i], proximo])
                posicao_atual += 1

        return indice_secundario, lista_invertida