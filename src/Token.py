class Token:
    def __init__(self, tipo, lexema, literal, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.literal = literal
        self.linha = linha
        self.coluna = coluna

    def __str__(self):
        return f"{self.tipo.name} {self.lexema}"