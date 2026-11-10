"""Latch D transparente, montado sobre um SRLatch."""

from gates.and_gate import And
from gates.not_gate import Not
from components.sr_latch import SRLatch


class DLatch:
    """Acompanha `d` enquanto `enable` está em nível alto; retém o valor quando cai."""

    def __init__(self, d, enable):
        not_d = Not(d)
        s = And(d, enable)
        r = And(not_d, enable)

        self._sr_latch = SRLatch(s, r)

    @property
    def output(self):
        return self._sr_latch.output

    def add_listener(self, listener):
        self._sr_latch.add_listener(listener)
