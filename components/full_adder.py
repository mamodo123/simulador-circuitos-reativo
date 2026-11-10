"""Somador completo de 1 bit, montado inteiramente com portas lógicas."""

from gates.xor_gate import Xor
from gates.and_gate import And
from gates.or_gate import Or


class FullAdder:
    """Soma dois bits e um carry de entrada, expondo `.sum` e `.carry_out`."""

    def __init__(self, a, b, carry_in):
        xor_ab = Xor(a, b)
        and_ab = And(a, b)
        and_xor_carry = And(xor_ab, carry_in)

        self.sum = Xor(xor_ab, carry_in)
        self.carry_out = Or(and_ab, and_xor_carry)
