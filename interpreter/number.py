class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def dived_by(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)

    def __repr__(self) -> str:
        return str(self.value)
