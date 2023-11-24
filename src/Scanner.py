from TokenTypes import TokenTypes
from Token import Token

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.comeco = 0
        self.atual = 0
        self.linha = 1
        self.coluna = 0

    PALRESERVADAS = {
        "public static void main(String[] args)": TokenTypes.MAIN_ID,
        "if": TokenTypes.IF_ID,
        "else": TokenTypes.ELSE_ID,
        "while": TokenTypes.WHILE_ID,
        "do": TokenTypes.DO_ID,
        "for": TokenTypes.FOR_ID,
        "int": TokenTypes.INT_ID,
        "float": TokenTypes.FLOAT_ID,
        "char": TokenTypes.CHAR_ID,
        ".lenght": TokenTypes.STRLEN,
        "System.out.print": TokenTypes.PRINT,
    }

    def scan_tokens(self):
        while not self.no_final():
            self.comeco = self.atual
            self.scan_token()
        self.tokens.append(Token(TokenTypes.EOF, "", None, self.linha, self.coluna))
        return self.tokens

    def no_final(self):
        return self.atual >= len(self.source)

    def advance(self):
        self.atual += 1
        self.coluna += 1
        return self.source[self.atual - 1]

    def add_token(self, tipo, literal=None):
        texto = self.source[self.comeco:self.atual]
        self.tokens.append(Token(tipo, texto, literal, self.linha, self.coluna))

    def match(self, expected):
        if self.no_final() or self.source[self.atual] != expected:
            return False
        self.atual += 1
        self.coluna += 1
        return True

    def look_ahead(self):
        if self.no_final():
            return '\0'
        return self.source[self.atual]

    def look_ahead_next(self):
        if self.atual + 1 >= len(self.source):
            return '\0'
        return self.source[self.atual + 1]

    def is_digit(self, c):
        return c >= '0' and c <= '9'

    def is_letter(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')

    def is_alpha(self, c):
        return self.is_letter(c) or c == '_'

    def identifier(self, c):
        while self.is_alpha_numeric(self.look_ahead()):
            self.advance()

        text = self.source[self.comeco:self.atual]

        if text == "public":
            text = ""
            while self.is_main(self.look_ahead()):
                self.advance()
            if not self.source[self.comeco:self.atual] == text:
                text += self.source[self.comeco:self.atual]
        elif text == "System":
            text = ""
            while self.is_sout(self.look_ahead()):
                self.advance()
            if not self.source[self.comeco:self.atual] == text:
                text += self.source[self.comeco:self.atual]
        tipo = self.PALRESERVADAS.get(text)
        if tipo is None:
            if self.is_digit(c) or c == '.':
                self.number(c)
            elif self.is_alpha(c):
                tipo = TokenTypes.IDENTIFICADOR
        self.add_token(tipo)

    def is_sout(self, c):
        return self.is_alpha(c) or self.is_digit(c) or self.is_dot(c)

    def is_main(self, c):
        return self.is_alpha(c) or self.is_digit(c) or c in {'(', ')', '[', ']', ' '}

    def is_dot(self, c):
        return c == '.'

    def scan_token(self):
        c = self.advance()
        if c == '"':
            self.add_token(TokenTypes.ASPAS)
        elif c == '[':
            self.add_token(TokenTypes.ABRE_COLCHETE)
        elif c == ']':
            self.add_token(TokenTypes.FECHA_COLCHETE)
        elif c == '(':
            self.add_token(TokenTypes.ABRE_PARENTESES)
        elif c == ')':
            self.add_token(TokenTypes.FECHA_PARENTESES)
        elif c == '{':
            self.add_token(TokenTypes.ABRE_CHAVE)
        elif c == '}':
            self.add_token(TokenTypes.FECHA_CHAVE)
        elif c == ',':
            self.add_token(TokenTypes.VIRGULA)
        elif c == '-':
            self.add_token(TokenTypes.SUBTRACAO)
        elif c == '+':
            self.add_token(TokenTypes.SOMA)
        elif c == ';':
            self.add_token(TokenTypes.PONTO_VIRGULA)
        elif c == '*':
            self.add_token(TokenTypes.MULTIPLICACAO)
        elif c == '=':
            self.add_token(TokenTypes.IGUAL if self.match('=') else TokenTypes.ATRIBUICAO)
        elif c == '<':
            self.add_token(TokenTypes.MENOR_IGUAL if self.match('=') else TokenTypes.MENOR)
        elif c == '>':
            self.add_token(TokenTypes.MAIOR_IGUAL if self.match('=') else TokenTypes.MAIOR)
        elif c == '&':
            if self.match('&'):
                self.add_token(TokenTypes.AND)
            else:
                print(f"ERRO: ('&') não seguida de '&' na linha: {self.linha} e coluna: {self.coluna}")
                exit(0)
        elif c == '|':
            if self.match('|'):
                self.add_token(TokenTypes.OR)
            else:
                print(f"ERRO: ('|') não seguida de '|' na linha: {self.linha} e coluna: {self.coluna}")
                exit(0)
        elif c == '!':
            if self.match('='):
                self.add_token(TokenTypes.DIFERENTE)
            else:
                print(f"ERRO: Exclamação ('!') não seguida de '=' na linha: {self.linha} e coluna: {self.coluna}")
                exit(0)
        elif c == '/':
            if self.match('/'):
                while self.look_ahead() != '\n' and not self.no_final():
                    self.advance()
            elif self.match('*'):
                coluna_erro = self.coluna
                start = self.linha
                while self.look_ahead_next() != '/' and not self.no_final():
                    if self.look_ahead() == '\n':
                        self.linha += 1
                        self.coluna = 0
                    self.advance()
                if self.no_final():
                    print(f"ERRO: Arquivo acabou com um comentário aberto na linha: {start} e coluna: {coluna_erro}")
                    exit(0)
                if self.look_ahead() == '*' and self.look_ahead_next() == '/':
                    self.advance()
                    self.advance()
            else:
                self.add_token(TokenTypes.DIVISAO)
        elif c == ' ':
            self.coluna += 0.5
        elif c == '\t':
            self.coluna += 4
        elif c == '\r' or c == '\n':
            self.linha += 1
            self.coluna = 0
        elif c == '\'':
            self.character(self.source[self.comeco + 1])
        else:
            if self.is_alpha(c) or self.is_digit(c) or c == '.':
                self.identifier(c)
            else:
                print(f"ERRO: Caracter Inválido({c}) na linha: {self.linha} e coluna: {self.coluna}")
                exit(0)

    def number(self, c):
        while self.is_digit(self.look_ahead()) and c != '.':
            self.advance()

        if c == '.':
            while self.is_digit(self.look_ahead()):
                self.advance()
            self.add_token(TokenTypes.FLOAT, float(self.source[self.comeco:self.atual]))
            return

        if self.look_ahead() == '.' and self.is_digit(self.look_ahead_next()):
            self.advance()
            while self.is_digit(self.look_ahead()):
                self.advance()
            self.add_token(TokenTypes.FLOAT, float(self.source[self.comeco:self.atual]))
        elif self.look_ahead() == '.' and not self.is_digit(self.look_ahead_next()):
            print(f"ERRO!: Float mal formado na linha: {self.linha} e coluna: {self.coluna}")
            self.advance()
            exit(0)
        else:
            self.add_token(TokenTypes.INT, int(self.source[self.comeco:self.atual]))

    def character(self, c):
        if self.is_digit(self.look_ahead()) or (self.is_letter(self.look_ahead()) and self.look_ahead_next() == "'"):
            self.advance()
            self.advance()
            self.add_token_char(TokenTypes.CHAR, c)
        else:
            print(f"Erro! Char mal formado na linha: {self.linha} e coluna: {self.coluna}")
            exit(0)

    def is_alpha_numeric(self, char):
        return self.is_alpha(char) or self.is_digit(char)


