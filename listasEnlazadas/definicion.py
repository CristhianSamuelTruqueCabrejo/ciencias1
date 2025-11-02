class Definicion:
    def __init__(self, num: int):
        self.num: int = num
        self.sig: 'Definicion' | None = None