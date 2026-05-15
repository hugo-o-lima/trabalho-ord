import sys
import os

from src.services.interpretador import Interpretador
from src.services.construtor_indices import ConstrutorIndices

def main():
    interpretador = Interpretador()
    construtor = ConstrutorIndices()

    jogos_string = interpretador.ler_arquivo("games.dat")
    lst_jogos = interpretador.split_arquivo(jogos_string)

    #FODASE CANSEI DPS EU FAÇO MAIS

if __name__=='__main__':
    main()