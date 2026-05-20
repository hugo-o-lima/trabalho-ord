import sys
import os

from src.services.interpretador import Interpretador
from src.services.construtor_indices import ConstrutorIndices

def main():
    construtor = ConstrutorIndices()
    interpretador = Interpretador("operacoes")
    interpretador.carregar_todos_os_indices()

    arg1 = sys.argv[1]
    if not arg1:
        print("Funcionalidade não encontrada. Use '-b' para construir indices, '-e' para rodar operacoes ou '-c' para compactar arquivo.")

    if arg1 == "-b":
        construtor.construir_indices()
    if arg1 == "-e":
        pass
    else:
        print("Funcionalidade não existe, tente novamente usando '-b', '-e' ou '-c'.")

if __name__=='__main__':
    main()