import sys
import os

from src.services.interpretador import Interpretador
from src.services.construtor_indices import ConstrutorIndices
from src.services.processador_operacoes import ProcessadorOperacoes

def main():
    construtor = ConstrutorIndices()
    if len(sys.argv)>2:
        interpretador = Interpretador(sys.argv[2])
    else:
        interpretador = Interpretador()
    processador = ProcessadorOperacoes()


    if len(sys.argv)<2:
        print("Funcionalidade não encontrada. Use '-b' para construir indices, '-e' para rodar operacoes ou '-c' para compactar arquivo.")

    arg1 = sys.argv[1]
    if arg1 == "-b":
        construtor.construir_indices()
    elif arg1 == "-e":
        operacoes = interpretador.interpretar_operacoes()
        if len(operacoes)==0:
            print("Erro: não foi possível processar o arquivo de operações.")
            return
        
        interpretador.carregar_todos_os_indices()
        
        for codigo_op, argumento in operacoes:
            if codigo_op == 4:
                processador.remover_registro(argumento, interpretador)

        interpretador.salvar_todos_os_indices()

    elif arg1 == "-c":
        interpretador.carregar_todos_os_indices()
    else:
        print("Funcionalidade não existe, tente novamente usando '-b', '-e' ou '-c'.")

if __name__=='__main__':
    main()