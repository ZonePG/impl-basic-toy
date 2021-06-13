from error import RTError


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
            return Number(self.value + other.value), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, "Divsion by zero")
            return Number(self.value / other.value), None

    def __repr__(self) -> str:
        return str(self.value)
