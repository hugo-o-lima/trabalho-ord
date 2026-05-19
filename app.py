import sys
import os

from src.services.interpretador import Interpretador
from src.services.construtor_indices import ConstrutorIndices

def main():
    interpretador = Interpretador()
    construtor = ConstrutorIndices()

    if sys.argv[1] == "-b":
        construtor.construir_indices()

if __name__=='__main__':
    main()