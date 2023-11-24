class VarList:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def add(self, novo):
        novo.next = self.inicio
        self.inicio = novo

        if self.fim is None:
            self.fim = novo

    def existe(self, no):
        iterador = self.inicio

        while iterador is not None:
            if (
                iterador.literal == no.literal
                and iterador.tipo == no.tipo
                and iterador.bloco == no.bloco
            ):
                return True

            iterador = iterador.next

        return False

    def find(self, literal, bloco):
        iterador = self.inicio

        while iterador is not None:
            if iterador.literal == literal and iterador.bloco <= bloco:
                return iterador

            iterador = iterador.next

        return None

    def __str__(self):
        lista = ""
        iterador = self.inicio

        while iterador is not None:
            lista += f"{iterador.tipo} {iterador.literal} {iterador.bloco} {iterador.valorNumerico} {iterador.valorString}\n"
            iterador = iterador.next

        return lista

    def removerBloco(self, bloco):
        iterador = self.inicio
        while iterador is not None:
            if iterador.bloco == bloco:
                self.remover(iterador)
                iterador = self.inicio
                continue
            iterador = iterador.next

    def remover(self, no):
        anterior = None
        iterador = self.inicio
        while iterador is not None:
            if iterador.bloco == no.bloco:
                if anterior is not None:
                    anterior.next = iterador.next
                else:
                    self.inicio = iterador.next
                iterador.next = None
                return
            anterior = iterador
            iterador = iterador.next
