import math

class ProcessadorOperacoes:
    def __init__(self):
        lst = [1, 3, 6, 9, 12, 30]
        print(self.busca_binaria(lst, 8))

    def busca_binaria(self, lst_indices, indice_buscado):
        if len(lst_indices) <= 1:
            print(f"Erro: indice ({indice_buscado}) buscado não foi encontrado.")
            return -1
        
        metade = math.floor(len(lst_indices)/2)
        if lst_indices[metade] == indice_buscado:
            return metade
        elif lst_indices[metade] > indice_buscado:
            return self.busca_binaria(lst_indices[:metade], indice_buscado)
        else:
            return self.busca_binaria(lst_indices[metade:], indice_buscado)