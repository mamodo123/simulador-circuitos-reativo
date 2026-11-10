"""Somador de N bits, encadeando FullAdder bit a bit."""

from signals.bit_array import BitArray
from signals.bit_slice import BitSlice
from signals.bus import Bus
from components.full_adder import FullAdder


class RippleCarryAdder:
    """Soma dois barramentos de N bits; overflow aparece em `.carry_out`, não em `.sum`."""

    def __init__(self, a, b, carry_in=None):
        width = len(a.output)
        carry = carry_in if carry_in is not None else BitArray([False])

        sum_bits = [None] * width
        self.full_adders = []
        for i in range(width - 1, -1, -1):
            bit_a = BitSlice(a, i)
            bit_b = BitSlice(b, i)
            full_adder = FullAdder(bit_a, bit_b, carry)
            self.full_adders.append(full_adder)
            sum_bits[i] = full_adder.sum
            carry = full_adder.carry_out

        self.sum = Bus(sum_bits)
        self.carry_out = carry
