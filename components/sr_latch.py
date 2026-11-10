"""Latch SR de NOR cruzadas: o elemento de memória mais simples do simulador."""

from signals.bit_array import BitArray
from gates.nor_gate import Nor


class SRLatch:
    """Retém 1 bit via realimentação combinacional; S=R=1 é combinação inválida."""

    def __init__(self, s, r):
        q_not_proxy = BitArray([False])

        self.q = Nor(r, q_not_proxy)
        self.q_not = Nor(s, self.q)

        self.q_not.add_listener(q_not_proxy.trigger_change)
        q_not_proxy.output = self.q_not.output

    @property
    def output(self):
        return self.q.output

    def add_listener(self, listener):
        self.q.add_listener(listener)
