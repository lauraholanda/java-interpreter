from TokenTypes import TokenTypes
from VarList import VarList as lista
from VarNode import VarNode 
class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.look = None
        self.tokenIt = 0
        self.bloco = 0
        self.tipo = None

    def nextTk(self):
        self.tokenIt += 1
        self.look = self.tokens[self.tokenIt]
        if self.match(None):
            self.nextTk()

    def lookAhead(self, n):
        return self.tokens[self.tokenIt + n]

    def lookBehind(self, n):
        return self.tokens[self.tokenIt - n]

    def match(self, tipo):
        return self.look.tipo == tipo

    def error(self, msg):
        print(f"Erro!\n{msg}\nUltimo Token lido: {self.look} na linha: {self.look.linha} e coluna: {self.look.coluna}")
        exit(0)

    def programa(self):
        self.look = self.tokens[self.tokenIt]
        if self.match(TokenTypes.MAIN_ID):
            self.nextTk()
            self.bloco()
        else:
            self.error("Não especificou o Main")

    def bloco(self):
        if self.match(TokenTypes.ABRE_CHAVE):
            self.bloco += 1
            self.nextTk()
            while self.match(TokenTypes.INT_ID) or self.match(TokenTypes.FLOAT_ID) or self.match(TokenTypes.CHAR_ID):
                self.decl_var()
            while self.match(TokenTypes.IDENTIFICADOR) or self.match(TokenTypes.WHILE_ID) or \
                    self.match(TokenTypes.DO_ID) or self.match(TokenTypes.IF_ID) or self.match(TokenTypes.FOR_ID) or \
                    self.match(TokenTypes.PRINT) or self.match(TokenTypes.STRLEN):
                self.comando()
            if not self.match(TokenTypes.FECHA_CHAVE):
                self.error("Bloco mal formado")
            lista.removerBloco(self.bloco)
            self.bloco -= 1
        else:
            self.error("Bloco mal formado")

    def decl_var(self):
        self.tipo()
        self.tipo = self.look.tipo
        self.nextTk()
        self.id()
        self.tipo = None

    def tipo(self):
        if not (self.match(TokenTypes.INT_ID) or self.match(TokenTypes.FLOAT_ID) or self.match(TokenTypes.CHAR_ID)):
            self.error("Especificação do tipo da variavel errada")

    def id(self):
        id = self.look.lexema
        if self.match(TokenTypes.IDENTIFICADOR):
            lista.add(VarNode(self.tipo, self.look.lexema, self.bloco))
            self.nextTk()
            while self.match(TokenTypes.VIRGULA):
                self.nextTk()
                if self.match(TokenTypes.IDENTIFICADOR):
                    lista.add(VarNode(self.tipo, self.look.lexema, self.bloco))
                    self.nextTk()
                else:
                    self.error("Objeto inesperado depois da vírgula")
            if self.match(TokenTypes.ABRE_COLCHETE):
                self.nextTk()
                if self.match(TokenTypes.INT) or self.match(TokenTypes.IDENTIFICADOR):
                    lista.find(id, self.bloco).arraySize = int(self.look.lexema)
                    self.nextTk()
                    if self.match(TokenTypes.FECHA_COLCHETE):
                        self.nextTk()
                elif self.match(TokenTypes.FECHA_COLCHETE):
                    self.nextTk()
            if self.match(TokenTypes.ATRIBUICAO):
                self.nextTk()
                if self.match(TokenTypes.INT) or self.match(TokenTypes.IDENTIFICADOR):
                    lista.find(id, self.bloco).arraySize = int(self.look.lexema)
                    self.nextTk()
                else:
                    print("Erro na atribuição")
            if not self.match(TokenTypes.PONTO_VIRGULA):
                self.error("Erro no ponto e virgula")
            self.nextTk()
        else:
            self.error("Identificador não encontrado!")

    def comando(self):
        if self.match(TokenTypes.IDENTIFICADOR) or self.match(TokenTypes.ABRE_CHAVE):
            self.comando_basico()
        elif self.match(TokenTypes.WHILE_ID) or self.match(TokenTypes.DO_ID):
            self.iteracao()
        elif self.match(TokenTypes.FOR_ID):
            self.iteracaoFor()
        elif self.match(TokenTypes.PRINT):
            self.print_()
        elif self.match(TokenTypes.STRLEN):
            self.strlen(True)
        elif self.match(TokenTypes.IF_ID):
            self.nextTk()
            if self.match(TokenTypes.ABRE_PARENTESES):
                if self.opr_logica():
                    if self.match(TokenTypes.FECHA_PARENTESES):
                        self.nextTk()
                        self.comando()
                        self.nextTk()
                        if self.match(TokenTypes.ELSE_ID):
                            self.nextTk()
                            if not self.opr_logica():
                                self.skipComando()
                        return
                    else:
                        self.error("Não fechou parenteses na condição do IF")
                else:
                    self.error("Operação lógica mal formada")
            else:
                self.error("Não abriu parenteses na condição do IF")
        else:
            self.error("Comando não reconhecido")

    def skipComando(self):
        chave = 1
        while chave != 0:
            self.nextTk()
            if self.match(TokenTypes.ABRE_CHAVE):
                chave += 1
            if self.match(TokenTypes.FECHA_CHAVE):
                chave -= 1
    
    def comando_basico(self):
        if self.match(TokenTypes.IDENTIFICADOR):
            self.atribuicao(False)
        elif self.match(TokenTypes.ABRE_CHAVE):
            self.bloco()

    def atribuicao(self, pularPV):
        if self.match(TokenTypes.IDENTIFICADOR):
            var = self.look
            valor = 0
            valorString = ""
            self.nextTk()
            if self.match(TokenTypes.ABRE_COLCHETE):
                self.nextTk()
                if self.match(TokenTypes.FECHA_COLCHETE):
                    self.nextTk()
                    if self.match(TokenTypes.ATRIBUICAO):
                        self.nextTk()
                        if self.match(TokenTypes.ASPAS):
                            self.nextTk()
                            while not self.match(TokenTypes.ASPAS):
                                valorString += " " + self.look.lexema
                                self.nextTk()
                            self.nextTk()
                            if self.match(TokenTypes.PONTO_VIRGULA):
                                lista.find(var.lexema, self.bloco).setValor(valorString)
                                return
                        else:
                            self.error("Cadeia de caracteres mal formada")
                    else:
                        self.error("Operador de atribuição faltando")
                else:
                    self.error("Não fechou colchete na atribuição")
            elif self.match(TokenTypes.ATRIBUICAO):
                valor = self.op_aritmetica()
                lista.find(var.lexema, self.bloco).valorNumerico = valor
                if self.match(TokenTypes.PONTO_VIRGULA):
                    self.nextTk()
                elif not pularPV:
                    self.error("Ponto e vírgula no lugar errado")
            else:
                self.error("Sinal de atribuição faltando")
        else:
            self.error("Identificador não encontrado")

    def iteracao(self):
        tokenPosition = 0
        finalTokenPosition = 0
        if self.match(TokenTypes.WHILE_ID):
            self.nextTk()
            if self.match(TokenTypes.ABRE_PARENTESES):
                tokenPosition = self.tokenIt
                while self.opr_logica():
                    if self.match(TokenTypes.FECHA_PARENTESES):
                        finalTokenPosition = self.tokenIt
                        self.nextTk()
                        self.comando()
                        self.nextTk()
                        self.tokenIt = tokenPosition
                        self.look = self.tokens[self.tokenIt]
                self.nextTk()
                self.skipComando()
                self.nextTk()
            else:
                self.error("Parentese da condição do while não foi aberto")
        elif self.match(TokenTypes.DO_ID):
            self.nextTk()
            self.comando()
            if self.match(TokenTypes.FECHA_CHAVE):
                self.nextTk()
                if self.match(TokenTypes.WHILE_ID):
                    self.nextTk()
                    if self.match(TokenTypes.ABRE_PARENTESES):
                        self.expr_relacional()
                        if self.match(TokenTypes.FECHA_PARENTESES):
                            self.nextTk()
                            if not self.match(TokenTypes.PONTO_VIRGULA):
                                self.error("Falta ponto e vírgula depois do while")
                            self.nextTk()
                        else:
                            self.error("Não fechou parenteses")
                    else:
                        self.error("Não abriu parenteses da condição do while")
                else:
                    self.error("Não forneceu a condição do DO")
            else:
                self.error("Não fechou o bloco do DO")

    def iteracaoFor(self):
        tokenPosition = 0
        finalTokenPosition = 0
        if self.match(TokenTypes.FOR_ID):
            self.nextTk()
            if self.match(TokenTypes.ABRE_PARENTESES):
                self.nextTk()
                self.atribuicao(False)
                tokenPosition = self.tokenIt - 1
                while self.expr_relacional():
                    if self.match(TokenTypes.PONTO_VIRGULA):
                        self.nextTk()
                        self.atribuicao(True)
                        if self.match(TokenTypes.FECHA_PARENTESES):
                            finalTokenPosition = self.tokenIt
                            self.nextTk()
                            self.bloco()
                    self.tokenIt = tokenPosition
                    self.look = self.tokens[self.tokenIt]
                self.tokenIt = finalTokenPosition + 1
                self.look = self.tokens[self.tokenIt]
                self.skipComando()
                self.nextTk()
            else:
                self.error("Parentese da condição do for não foi aberto")

    def opr_logica(self):
        actual = self.expr_relacional()
        if self.match(TokenTypes.AND):
            recursive = self.opr_logica()
            return actual and recursive
        elif self.match(TokenTypes.OR):
            recursive = self.opr_logica()
            if not self.match(TokenTypes.FECHA_PARENTESES):
                return actual
            return actual or recursive
        return actual

    def expr_relacional(self):
        op_ari1 = self.op_aritmetica()
        tipo = self.op_relacional()
        op_ari2 = self.op_aritmetica()

        if tipo == TokenTypes.MENOR_IGUAL:
            return op_ari1 <= op_ari2
        elif tipo == TokenTypes.MENOR:
            return op_ari1 < op_ari2
        elif tipo == TokenTypes.MAIOR_IGUAL:
            return op_ari1 >= op_ari2
        elif tipo == TokenTypes.MAIOR:
            return op_ari1 > op_ari2
        elif tipo == TokenTypes.IGUAL:
            return op_ari1 == op_ari2
        elif tipo == TokenTypes.DIFERENTE:
            return op_ari1 != op_ari2
        return False

    def op_relacional(self):
        if not (self.match(TokenTypes.MENOR_IGUAL) or self.match(TokenTypes.MENOR) or
                self.match(TokenTypes.MAIOR_IGUAL) or self.match(TokenTypes.MAIOR) or
                self.match(TokenTypes.IGUAL) or self.match(TokenTypes.DIFERENTE)):
            self.error("Operador relacional não existente")
        return self.look.tipo

    def op_aritmetica(self):
        result = 0
        termo_value = self.termo()
        result = self.somaOuSubtracao(termo_value)
        return result

    def termo(self):
        result = 0
        fator_value = self.fator()
        result = self.multiplicacaoOuDivisao(fator_value)
        return result
    
    def fator(self):
            valor = 0
            self.nextTk()
            if self.match(TokenTypes.STRLEN):
                valor = self.strlen(False)
            elif self.match(TokenTypes.IDENTIFICADOR) or self.match(TokenTypes.INT) or self.match(TokenTypes.FLOAT) or \
                    self.match(TokenTypes.CHAR):
                if self.match(TokenTypes.IDENTIFICADOR):
                    valor = self.lista.find(self.look.lexema, self.bloco).valorNumerico
                else:
                    valor = float(self.look.lexema)
                self.nextTk()
                return valor
            elif self.match(TokenTypes.ABRE_PARENTESES):
                valor = self.op_aritmetica()
                if self.match(TokenTypes.FECHA_PARENTESES):
                    self.nextTk()
                    return valor
                else:
                    self.error("Não fechou parênteses na expressão aritmética")
            elif self.match(TokenTypes.MULTIPLICACAO) or self.match(TokenTypes.DIVISAO) or self.match(TokenTypes.SOMA) or self.match(TokenTypes.SUBTRACAO) or self.match(TokenTypes.PONTO_VIRGULA):
                    self.error("Operador inválido na expressão aritmética")
            return valor
            
    def multiplicacaoOuDivisao(self, first):
        if self.match(TokenTypes.MULTIPLICACAO) or self.match(TokenTypes.DIVISAO):
            tipo = self.look.tipo
            second = self.fator()
            result = 0
            if tipo == TokenTypes.MULTIPLICACAO:
                result = first * second
            else:
                result = first / second
            return self.multiplicacaoOuDivisao(result)
        return first

    def somaOuSubtracao(self, first):
        if self.match(TokenTypes.SOMA) or self.match(TokenTypes.SUBTRACAO):
            tipo = self.look.tipo
            second = self.fator()
            result = 0
            if tipo == TokenTypes.SOMA:
                result = first + second
            else:
                result = first - second
            return self.somaOuSubtracao(result)
        return first

    @staticmethod
    def printLista():
        print(Interpreter.lista.toString())

    def print_(self):
        var = ""
        self.nextTk()
        if self.match(TokenTypes.ABRE_PARENTESES):
            self.nextTk()
            if self.match(TokenTypes.ASPAS):
                self.nextTk()
                while not self.match(TokenTypes.ASPAS):
                    var += " " + self.look.lexema
                    self.nextTk()
                if self.match(TokenTypes.ASPAS):
                    self.nextTk()
                else:
                    self.error("Não fechou aspas do print")
            elif self.match(TokenTypes.IDENTIFICADOR):
                if self.lookAhead(1).tipo == TokenTypes.ASPAS:
                    self.error("Print mal formado")
                elif self.lookAhead(1).tipo == TokenTypes.STRLEN:
                    self.nextTk()
                    var += self.strlen(False)
                else:
                    var = self.lista.find(self.look.lexema, self.bloco).getString()
                    self.nextTk()
            elif self.match(TokenTypes.STRLEN):
                var += self.strlen(False)
            if self.match(TokenTypes.FECHA_PARENTESES):
                print(var)
                self.nextTk()
                if self.match(TokenTypes.PONTO_VIRGULA):
                    self.nextTk()
                    return
                else:
                    self.error("Falta de ponto e vírgula")
            else:
                self.error("Não fechou parênteses do print")
        else:
            self.error("Não abriu parênteses no print")

    def strlen(self, pv):
        print(self.lookBehind(1).lexema)
        size_value = self.lista.find(self.lookBehind(1).lexema, self.bloco).getArraySize()
        self.nextTk()
        if self.match(TokenTypes.ABRE_PARENTESES):
            self.nextTk()
            if self.match(TokenTypes.FECHA_PARENTESES):
                self.nextTk()
                if pv:
                    if self.match(TokenTypes.PONTO_VIRGULA):
                        self.nextTk()
                        return size_value
                    else:
                        self.error("Falta de ponto e vírgula")
                else:
                    return size_value
            else:
                self.error("Não fechou parênteses do print")
        else:
            self.error("Não abriu parênteses no print")
        return size_value
