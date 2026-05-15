import os

class Interpretador:
    def __init__(self) -> None:
        pass

    def ler_arquivo(self, caminho: str) -> str:
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Não foi encontrado arquivo {caminho}.")
        
        arquivo = open(caminho, 'rb')

        dados = arquivo.read()
        dados_decodificados = dados.decode("utf-8")

        arquivo.close()
        return dados_decodificados

    def split_arquivo(self, conteudo: str) -> list[list[str]]:
            if not conteudo:
                raise ValueError("Arquivo está vazio.")

            lst_jogos = []    
            
            blocos = conteudo.split('\x00')

            for i in range(1, len(blocos)):
                bloco = blocos[i]
                
                if "|" in bloco:
                    campos = bloco.split('|')

                    if i < len(blocos) - 1 and len(campos[-1]) > 0:
                        campos[-1] = campos[-1][:-1]
                    
                    lista_campos = []
                    for campo in campos:
                        valor = campo.strip()
                        if valor:
                            lista_campos.append(valor)

                    if lista_campos:
                        lst_jogos.append(lista_campos)
            
            return lst_jogos
