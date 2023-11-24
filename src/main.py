import io
from Scanner import Scanner
from Interpretador import Interpreter
from TokenTypes import TokenTypes
import sys


def main():
    try:
        run_file("test.txt")
        
        if len(sys.argv) > 1:
            run_file(sys.argv[1])
        else:
            print("Compilou com sucesso.")
    except Exception as e:
        print(f"Erro: {e}")

def run_file(path):
    with open(path, 'r') as file:
        source = file.read()
        run(source)

def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    interpreter = Interpreter(tokens)
    interpreter.programa()
if __name__ == "__main__":
    main()
