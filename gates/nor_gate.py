"""Porta lógica NOR, composta a partir de OR e NOT."""

from gates.or_gate import Or
from gates.not_gate import Not


class Nor:
    """Nega a saída de uma porta OR; base do latch SR (components/sr_latch.py)."""

    def __init__(self, a, b):
        self._or = Or(a, b)
        self._not = Not(self._or)

    @property
    def output(self):
        return self._not.output

    def add_listener(self, listener):
        self._not.add_listener(listener)
