"""Testes automatizados que reproduzem as validações do Capítulo 5 do TCC.

Executar a partir da raiz do projeto:  python -m unittest discover -s tests -t .
"""

import unittest
from itertools import product

from signals.bit_array import BitArray
from gates.not_gate import Not
from gates.and_gate import And
from gates.xor_gate import Xor
from components.behavioral_adder import BehavioralAdder
from components.full_adder import FullAdder
from components.ripple_carry_adder import RippleCarryAdder
from components.behavioral_register import BehavioralRegister
from components.sr_latch import SRLatch
from components.d_flip_flop import DFlipFlop
from components.d_flip_flop_register import DFlipFlopRegister


def bits(text):
    """'101' -> [True, False, True]"""
    return [c == "1" for c in text]


def pulse(clock, low=False, high=True):
    clock.output = low
    clock.output = high


class TestPortas(unittest.TestCase):
    def test_not_reativo(self):
        a = BitArray(bits("010"))
        not_a = Not(a)
        self.assertEqual(not_a.output, bits("101"))
        a.output = bits("111")
        self.assertEqual(not_a.output, bits("000"))

    def test_meio_somador(self):
        for x, y in product([False, True], repeat=2):
            bx, by = BitArray([x]), BitArray([y])
            self.assertEqual(Xor(bx, by).output, [x != y])
            self.assertEqual(And(bx, by).output, [x and y])

    def test_somador_completo(self):
        for a, b, c in product([0, 1], repeat=3):
            fa = FullAdder(BitArray([bool(a)]), BitArray([bool(b)]), BitArray([bool(c)]))
            total = a + b + c
            self.assertEqual(fa.sum.output, [bool(total % 2)])
            self.assertEqual(fa.carry_out.output, [total >= 2])

    def test_ripple_carry_adder_exaustivo(self):
        for x, y in product(range(8), repeat=2):
            a = BitArray(bits(format(x, "03b")))
            b = BitArray(bits(format(y, "03b")))
            adder = RippleCarryAdder(a, b)
            self.assertEqual(adder.sum.output, bits(format((x + y) % 8, "03b")))
            self.assertEqual(adder.carry_out.output, [x + y >= 8])


class TestBehavioralRegister(unittest.TestCase):
    def test_captura_somente_na_borda_de_subida(self):
        data = BitArray([True])
        clock = BitArray(False)
        register = BehavioralRegister(clock, data)
        self.assertIsNone(register.output)
        clock.output = True
        self.assertEqual(register.output, [True])
        data.output = [False]
        self.assertEqual(register.output, [True])
        clock.output = False
        self.assertEqual(register.output, [True])

    def test_clock_em_lista_nao_captura_na_descida(self):
        # Regressão: com clock [bool], a lista [False] é "verdadeira" em Python
        # e a versão anterior capturava também na borda de descida.
        data = BitArray([True])
        clock = BitArray([False])
        register = BehavioralRegister(clock, data)
        clock.output = [True]
        self.assertEqual(register.output, [True])
        data.output = [False]
        clock.output = [False]
        self.assertEqual(register.output, [True])
        clock.output = [True]
        self.assertEqual(register.output, [False])


class TestContadores(unittest.TestCase):
    def test_contador_behavioral_adder_com_overflow(self):
        increment = BitArray(bits("001"))
        value = BitArray(bits("000"))
        clock = BitArray(False)
        counter = BehavioralRegister(clock, BehavioralAdder(increment, value), feedback_target=value)
        for i in range(1, 10):
            pulse(clock)
            self.assertEqual(counter.output, bits(format(i % 8, "03b")))

    def test_contador_portas_com_carry_out(self):
        increment = BitArray(bits("001"))
        value = BitArray(bits("000"))
        adder = RippleCarryAdder(value, increment)
        clock = BitArray(False)
        counter = BehavioralRegister(clock, adder.sum, feedback_target=value)
        for i in range(1, 10):
            pulse(clock)
            self.assertEqual(counter.output, bits(format(i % 8, "03b")))
            self.assertEqual(adder.carry_out.output, [i % 8 == 7])

    def test_contador_registrador_real(self):
        increment = BitArray(bits("001"))
        value = BitArray(bits("000"))
        adder = RippleCarryAdder(value, increment)
        clock = BitArray([False])
        counter = DFlipFlopRegister(clock, adder.sum, feedback_target=value)
        # Valor inicial fixado pelo proxy dos SRLatch internos (111).
        self.assertEqual(counter.output, bits("111"))
        for i in range(1, 10):
            pulse(clock, [False], [True])
            self.assertEqual(counter.output, bits(format((i + 7) % 8, "03b")))


class TestLatches(unittest.TestCase):
    def test_sr_latch(self):
        s, r = BitArray([True]), BitArray([False])
        latch = SRLatch(s, r)
        self.assertEqual(latch.output, [True])
        s.output = [False]
        self.assertEqual(latch.output, [True])
        r.output = [True]
        self.assertEqual(latch.output, [False])
        r.output = [False]
        self.assertEqual(latch.output, [False])

    def test_d_flip_flop_borda_de_subida(self):
        d, clock = BitArray([False]), BitArray([False])
        ff = DFlipFlop(d, clock)
        d.output = [True]
        clock.output = [True]
        self.assertEqual(ff.output, [True])
        d.output = [False]
        self.assertEqual(ff.output, [True])
        clock.output = [False]
        self.assertEqual(ff.output, [True])
        clock.output = [True]
        self.assertEqual(ff.output, [False])

    def test_toggle_behavioral_register(self):
        clock, signal = BitArray(False), BitArray([False])
        BehavioralRegister(clock, Xor(signal, BitArray([True])), feedback_target=signal)
        for i in range(1, 7):
            pulse(clock)
            self.assertEqual(signal.output, [i % 2 == 1])

    def test_toggle_d_flip_flop(self):
        clock, signal = BitArray([False]), BitArray([False])
        DFlipFlop(Not(signal), clock, feedback_target=signal)
        self.assertEqual(signal.output, [True])
        for i in range(1, 7):
            pulse(clock, [False], [True])
            self.assertEqual(signal.output, [i % 2 == 0])


if __name__ == "__main__":
    unittest.main()
