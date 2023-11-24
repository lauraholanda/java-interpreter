class VarNode:
    def __init__(self, tipo=None, literal=None, bloco=None, valorNumerico=0, valorString=""):
        self.next = None
        self.tipo = tipo
        self.literal = literal
        self.bloco = bloco
        self.valorNumerico = valorNumerico
        self.valorString = valorString
        self.arraySize = 0
        self.arrayList = None

    def get_string(self):
        if self.valorString != "":
            return self.valorString
        else:
            return str(self.valorNumerico)

    def set_valor(self, input):
        try:
            dbl = float(input)
            self.valorNumerico = dbl
            return True
        except ValueError:
            self.valorString = input
            return True

    def create_list(self, size):
        self.arrayList = [None] * size
        self.arraySize = size

    def get_array_size(self):
        return self.arraySize
